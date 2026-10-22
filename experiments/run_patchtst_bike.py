"""Quick PatchTST ablation on UCI Bike Sharing.

Usage:
    python experiments/run_patchtst_bike.py --epochs 15 --seeds 13 42 2026

The experiment is intentionally small and CPU-friendly. It forecasts the next
24 hourly bike counts from the previous 168 hours using a univariate target.
The only architectural change between the two neural variants is LayerNorm
immediately after the 1-D linear patch projection.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "eda" / "data" / "raw" / "hour.csv"
OUT = ROOT / "experiments" / "results"


@dataclass
class Config:
    context: int = 168
    horizon: int = 24
    patch_len: int = 24
    stride: int = 24
    d_model: int = 32
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 64
    dropout: float = 0.1
    batch_size: int = 128
    epochs: int = 15
    patience: int = 4
    lr: float = 1e-3
    weight_decay: float = 1e-4


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def load_hourly_target() -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    if not DATA.exists():
        raise FileNotFoundError(
            f"Missing {DATA}. Run `python eda/scripts/download_data.py` first."
        )
    raw = pd.read_csv(DATA)
    timestamps = pd.to_datetime(raw["dteday"]) + pd.to_timedelta(raw["hr"], unit="h")
    s = pd.Series(raw["cnt"].to_numpy(dtype=np.float32), index=timestamps)
    full_idx = pd.date_range(s.index.min(), s.index.max(), freq="h")
    observed = s.reindex(full_idx)
    observed_mask = observed.notna().to_numpy()
    # Forward fill never uses future observations. There are no leading gaps.
    filled = observed.ffill().bfill().to_numpy(dtype=np.float32)
    return filled, observed_mask, full_idx


def make_windows(
    values: np.ndarray,
    observed_mask: np.ndarray,
    start: int,
    end: int,
    context: int,
    horizon: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs, ys, ms = [], [], []
    first = max(context, start)
    last = end - horizon
    for target_start in range(first, last + 1):
        xs.append(values[target_start - context : target_start])
        ys.append(values[target_start : target_start + horizon])
        ms.append(observed_mask[target_start : target_start + horizon])
    return (
        np.asarray(xs, dtype=np.float32),
        np.asarray(ys, dtype=np.float32),
        np.asarray(ms, dtype=np.float32),
    )


class PatchTST(nn.Module):
    def __init__(self, cfg: Config, use_projection_ln: bool):
        super().__init__()
        n_patches = 1 + (cfg.context - cfg.patch_len) // cfg.stride
        self.patch_len = cfg.patch_len
        self.stride = cfg.stride
        self.projection = nn.Linear(cfg.patch_len, cfg.d_model)
        self.projection_ln = nn.LayerNorm(cfg.d_model) if use_projection_ln else nn.Identity()
        self.position = nn.Parameter(torch.zeros(1, n_patches, cfg.d_model))
        nn.init.normal_(self.position, std=0.02)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=cfg.d_model,
            nhead=cfg.n_heads,
            dim_feedforward=cfg.d_ff,
            dropout=cfg.dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=cfg.n_layers)
        self.head = nn.Linear(n_patches * cfg.d_model, cfg.horizon)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # [B, context] -> [B, patches, patch_len]
        patches = x.unfold(dimension=-1, size=self.patch_len, step=self.stride)
        z = self.projection_ln(self.projection(patches))
        z = self.encoder(z + self.position)
        return self.head(z.flatten(start_dim=1))


def masked_mse(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    weight = mask.sum().clamp_min(1.0)
    return (((pred - target) ** 2) * mask).sum() / weight


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer | None,
    device: torch.device,
) -> float:
    training = optimizer is not None
    model.train(training)
    losses = []
    for x, y, m in loader:
        x, y, m = x.to(device), y.to(device), m.to(device)
        with torch.set_grad_enabled(training):
            pred = model(x)
            loss = masked_mse(pred, y, m)
            if training:
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return float(np.mean(losses))


def predict(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    model.eval()
    preds, ys, masks = [], [], []
    with torch.no_grad():
        for x, y, m in loader:
            preds.append(model(x.to(device)).cpu().numpy())
            ys.append(y.numpy())
            masks.append(m.numpy())
    return np.concatenate(preds), np.concatenate(ys), np.concatenate(masks)


def metrics(pred: np.ndarray, target: np.ndarray, mask: np.ndarray, train_values: np.ndarray) -> dict[str, float]:
    p = pred[mask > 0.5]
    y = target[mask > 0.5]
    err = p - y
    denom = np.abs(p) + np.abs(y) + 1e-6
    train_diff = np.abs(np.diff(train_values))
    train_diff = train_diff[train_diff > 0]
    scale = float(np.mean(train_diff)) if len(train_diff) else 1.0
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err**2))),
        "smape_pct": float(100 * np.mean(2 * np.abs(err) / denom)),
        "mase": float(np.mean(np.abs(err)) / scale),
        "n_evaluated": int(len(y)),
    }


def baseline_predictions(x: np.ndarray, name: str, horizon: int) -> np.ndarray:
    if name == "naive_last":
        return np.repeat(x[:, -1:], horizon, axis=1)
    if name == "seasonal_naive_24":
        return x[:, -horizon:]
    raise ValueError(name)


def train_variant(
    variant: str,
    cfg: Config,
    seed: int,
    train: tuple[np.ndarray, np.ndarray, np.ndarray],
    val: tuple[np.ndarray, np.ndarray, np.ndarray],
    test: tuple[np.ndarray, np.ndarray, np.ndarray],
    mean: float,
    std: float,
    train_reference: np.ndarray,
    device: torch.device,
) -> dict[str, object]:
    seed_everything(seed)
    model = PatchTST(cfg, use_projection_ln=(variant == "patchtst_ln")).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    train_loader = DataLoader(TensorDataset(*[torch.from_numpy(a) for a in train]), batch_size=cfg.batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(*[torch.from_numpy(a) for a in val]), batch_size=cfg.batch_size)
    test_loader = DataLoader(TensorDataset(*[torch.from_numpy(a) for a in test]), batch_size=cfg.batch_size)
    best_state, best_val, best_epoch, stale = None, math.inf, 0, 0
    history = []
    started = time.time()
    for epoch in range(1, cfg.epochs + 1):
        train_loss = run_epoch(model, train_loader, optimizer, device)
        val_loss = run_epoch(model, val_loader, None, device)
        history.append({"epoch": epoch, "train_mse_scaled": train_loss, "val_mse_scaled": val_loss})
        if val_loss < best_val - 1e-7:
            best_val, best_epoch, stale = val_loss, epoch, 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            stale += 1
            if stale >= cfg.patience:
                break
    assert best_state is not None
    model.load_state_dict(best_state)
    p, y, m = predict(model, test_loader, device)
    p = p * std + mean
    y = y * std + mean
    result = {
        "variant": variant,
        "seed": seed,
        "best_epoch": best_epoch,
        "best_val_mse_scaled": best_val,
        "seconds": time.time() - started,
        "params": int(sum(v.numel() for v in model.parameters() if v.requires_grad)),
        **metrics(p, y, m, train_values=train_reference),
    }
    return {"result": result, "history": history}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--seeds", type=int, nargs="+", default=[13, 42, 2026])
    parser.add_argument("--threads", type=int, default=2)
    args = parser.parse_args()
    torch.set_num_threads(args.threads)
    cfg = Config(epochs=args.epochs)
    device = torch.device("cpu")
    values, observed_mask, idx = load_hourly_target()
    n = len(values)
    train_end, val_end = int(n * 0.70), int(n * 0.80)
    mean = float(values[:train_end].mean())
    std = float(values[:train_end].std())
    scaled = (values - mean) / std
    splits = {
        "train": make_windows(scaled, observed_mask, 0, train_end, cfg.context, cfg.horizon),
        "val": make_windows(scaled, observed_mask, train_end, val_end, cfg.context, cfg.horizon),
        "test": make_windows(scaled, observed_mask, val_end, n, cfg.context, cfg.horizon),
    }
    print(f"data points={n}, observed={observed_mask.sum()}, missing={len(observed_mask)-observed_mask.sum()}")
    print(f"splits: train={len(splits['train'][0])}, val={len(splits['val'][0])}, test={len(splits['test'][0])}")
    print(f"device={device}, config={asdict(cfg)}")

    OUT.mkdir(parents=True, exist_ok=True)
    all_results = []
    train_x, train_y, train_m = splits["train"]
    test_x, test_y, test_m = splits["test"]
    for name in ["naive_last", "seasonal_naive_24"]:
        pred = baseline_predictions(test_x * std + mean, name, cfg.horizon)
        result = {"variant": name, "seed": None, "best_epoch": None, "best_val_mse_scaled": None, "seconds": 0.0, "params": 0}
        result.update(metrics(pred, test_y * std + mean, test_m, train_values=values[:train_end]))
        all_results.append(result)
        print(result)

    details = []
    for variant in ["patchtst", "patchtst_ln"]:
        for seed in args.seeds:
            out = train_variant(variant, cfg, seed, splits["train"], splits["val"], splits["test"], mean, std, values[:train_end], device)
            all_results.append(out["result"])
            details.append(out)
            print(out["result"])

    results_df = pd.DataFrame(all_results)
    results_df.to_csv(OUT / "bike_patchtst_results.csv", index=False)
    payload = {
        "dataset": "UCI Bike Sharing hourly cnt",
        "source_file": str(DATA.relative_to(ROOT)),
        "time_range": [str(idx.min()), str(idx.max())],
        "n_full_hours": n,
        "n_observed_rows": int(observed_mask.sum()),
        "n_missing_hours": int((~observed_mask).sum()),
        "split_indices": {"train_end": train_end, "val_end": val_end, "n": n},
        "normalization": {"fit": "train only", "mean": mean, "std": std},
        "missing_target_policy": "forward-fill for regular input; exclude missing forecast labels from metrics",
        "config": asdict(cfg),
        "results": all_results,
        "histories": details,
    }
    (OUT / "bike_patchtst_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"saved {OUT / 'bike_patchtst_results.csv'}")
    print(f"saved {OUT / 'bike_patchtst_results.json'}")


if __name__ == "__main__":
    main()
