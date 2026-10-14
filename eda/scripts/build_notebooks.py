"""Sinh các notebook EDA (nguồn của notebooks/*.ipynb). Chạy lại nếu sửa nội dung."""
import nbformat as nbf, pathlib
NB = pathlib.Path(__file__).resolve().parents[1] / "notebooks"
SETUP = """import sys, pathlib, warnings
ROOT = pathlib.Path.cwd().parent if pathlib.Path.cwd().name == 'notebooks' else pathlib.Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from eda_utils import *
warnings.filterwarnings('ignore'); pd.set_option('display.width', 160); pd.set_option('display.max_columns', 30)
plt.rcParams['figure.dpi'] = 80
RAW = ROOT / 'data' / 'raw'
SUMMARY = {}  # các số chính, lưu ra reports/ để notebook so sánh dùng lại"""
SAVE = """import json; (ROOT/'reports').mkdir(exist_ok=True)
json.dump(SUMMARY, open(ROOT/'reports'/f"summary_{SUMMARY['dataset']}.json", 'w'), ensure_ascii=False, indent=1, default=str)
SUMMARY"""

def build(name, cells):
    nb = nbf.v4.new_notebook(); nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    for kind, src in cells:
        nb.cells.append(nbf.v4.new_markdown_cell(src) if kind == "md" else nbf.v4.new_code_cell(src))
    nbf.write(nb, NB / name)

M, C = "md", "code"

# ---------------------------------------------------------------- BIKE
build("eda_01_bike_sharing.ipynb", [
(M, """# EDA 1 — UCI Bike Sharing (UCI 275)
**Nguồn:** https://archive.ics.uci.edu/dataset/275 · **License:** CC BY 4.0 · **Paper gốc:** Fanaee-T & Gama (2014), *Event labeling combining ensemble detectors and background knowledge*, Progress in Artificial Intelligence 2(2–3):113–127, DOI 10.1007/s13748-013-0040-3.

Một chuỗi số lượt thuê xe theo giờ (Capital Bikeshare, Washington DC, 2011–2012), kèm thời tiết và lịch. Mục tiêu: `cnt`.

> Cách đọc: mỗi phần có ô code, rồi ô **Nhận xét** in ra từ chính số liệu vừa tính (không gõ tay số)."""),
(C, SETUP),
(M, "## 1. Đọc dữ liệu, shape, kiểu"),
(C, """df = pd.read_csv(RAW/'hour.csv')
df['t'] = pd.to_datetime(df['dteday']) + pd.to_timedelta(df['hr'], 'h')
print('shape:', df.shape); display(df.head(3)); display(overview(df))
SUMMARY.update(dataset='bike', rows=len(df), cols=df.shape[1]-1, freq='giờ', n_series=1)"""),
(M, "## 2. Khoảng thời gian, giờ thiếu, trùng lặp"),
(C, """g, missing = time_gaps(df['t'], 'h'); display(pd.Series(g))
miss_by_day = pd.Series(missing.date).value_counts()
print('Số ngày có giờ thiếu:', len(miss_by_day), '| ngày thiếu nhiều nhất:'); display(miss_by_day.head(5))
print('Dòng trùng hoàn toàn:', df.duplicated().sum(), '| NA tổng:', df.isna().sum().sum())
SUMMARY.update(start=g['start'], end=g['end'], missing_steps=g['n_missing_steps'], dup_ts=g['n_duplicated_ts'], n_na=int(df.isna().sum().sum()))"""),
(C, """print(f"Nhận xét: {g['n_missing_steps']} giờ thiếu trên {g['n_expected']} giờ kỳ vọng ({100*g['n_missing_steps']/g['n_expected']:.2f}%), "
      f"rải trên {len(miss_by_day)} ngày; ngày thiếu nhiều nhất {miss_by_day.index[0]} ({miss_by_day.iloc[0]} giờ). "
      f"Không có NA trong ô. Giờ thiếu thường là giờ không có lượt thuê/sự cố hệ thống → khi dựng lưới đều cần quyết định điền 0 hay nội suy.")"""),
(M, "## 3. Rò rỉ dữ liệu: `casual + registered = cnt`"),
(C, """leak = (df.casual + df.registered == df.cnt).mean()
print(f'Tỉ lệ dòng có casual+registered==cnt: {leak:.4f}')
print('Tương quan với cnt:', df[['casual','registered']].corrwith(df.cnt).round(3).to_dict())
SUMMARY['leak_cols'] = 'casual, registered'"""),
(C, """print(f"Nhận xét: {leak*100:.1f}% dòng thoả casual+registered=cnt → hai cột này là THÀNH PHẦN của mục tiêu, "
      "phải BỎ khỏi đặc trưng (nếu không, mô hình 'nhìn thấy đáp án'). Tương tự `instant` chỉ là số thứ tự, `dteday` đã mã hoá thành t.")"""),
(M, "## 4. Thống kê mô tả, phân phối, độ lệch"),
(C, """num = ['cnt','temp','atemp','hum','windspeed']
st = shape_stats(df[num]); display(st); plot_dists(df, num)
SUMMARY.update(target_mean=st.loc['cnt','mean'], target_skew=st.loc['cnt','skew'], target_kurt=st.loc['cnt','kurtosis'],
               target_cv=round(st.loc['cnt','std']/st.loc['cnt','mean'],3))
print('skew của log1p(cnt):', round(np.log1p(df.cnt).skew(),3))"""),
(C, """print(f"Nhận xét: cnt trung bình {st.loc['cnt','mean']:.1f}, trung vị {st.loc['cnt','50%']:.0f}, max {st.loc['cnt','max']:.0f}; "
      f"skew={st.loc['cnt','skew']:.2f}, kurtosis={st.loc['cnt','kurtosis']:.2f} → lệch phải. log1p đưa skew về {np.log1p(df.cnt).skew():.2f}. "
      "temp/atemp/hum/windspeed đã chuẩn hoá về [0,1] bởi nhà cung cấp.")"""),
(M, "## 5. Outlier (IQR 1.5)"),
(C, """out = iqr_outliers(df[num]); display(out)
SUMMARY['target_outlier_pct'] = out.loc['cnt','pct']
print(f"Nhận xét: {int(out.loc['cnt','n_outliers'])} giờ ({out.loc['cnt','pct']}%) có cnt vượt ngưỡng IQR {out.loc['cnt','upper']:.0f}; "
      "đây chủ yếu là giờ cao điểm thật, không phải lỗi → không nên xoá, cân nhắc biến đổi log.")"""),
(M, "## 6. Xu hướng & mùa vụ"),
(C, """s = df.set_index('t')['cnt']
fig, ax = plt.subplots(3,1, figsize=(12,8))
s.resample('D').sum().plot(ax=ax[0], title='Tổng theo ngày'); s.resample('W').sum().plot(ax=ax[0], secondary_y=True, alpha=.5)
df.groupby(['workingday','hr']).cnt.mean().unstack(0).plot(ax=ax[1], title='Trung bình theo giờ: ngày làm việc (1) vs nghỉ (0)')
df.groupby('mnth').cnt.mean().plot.bar(ax=ax[2], title='Trung bình theo tháng'); plt.tight_layout(); plt.show()
yr = df.groupby('yr').cnt.mean(); growth = yr[1]/yr[0]-1
print('TB/giờ theo năm:', yr.round(1).to_dict(), f'| tăng {growth*100:.1f}%')
SUMMARY['yoy_growth_pct'] = round(growth*100,1)"""),
(C, """sd = s.resample('D').sum()
strength_w = stl_strength(sd, period=7, title='STL chuỗi ngày (period=7)')
sh = s.asfreq('h').interpolate()  # chỉ cho STL; không dùng để huấn luyện
strength_d = stl_strength(sh, period=24, plot=False)
print('STL ngày (mùa tuần):', strength_w, '| STL giờ (mùa ngày):', strength_d)
SUMMARY.update(trend_strength=strength_w['trend_strength'], seasonal_strength=strength_d['seasonal_strength'])"""),
(C, """pk = df.groupby(['workingday','hr']).cnt.mean()
print(f"Nhận xét: TB/giờ năm 2012 cao hơn 2011 {growth*100:.1f}% → xu hướng tăng rõ (phân phối trôi theo thời gian). "
      f"Ngày làm việc: đỉnh sáng giờ {pk[1].loc[:11].idxmax()} ({pk[1].loc[:11].max():.0f}), đỉnh chiều giờ {pk[1].loc[12:].idxmax()} ({pk[1].loc[12:].max():.0f}); ngày nghỉ đỉnh giờ {pk[0].idxmax()} ({pk[0].max():.0f}). "
      f"Độ mạnh mùa ngày (STL period=24) = {strength_d['seasonal_strength']}, độ mạnh xu hướng chuỗi ngày = {strength_w['trend_strength']}.")"""),
(M, "## 7. ACF/PACF"),
(C, """acf_pacf(sh, lags=200, title='cnt (giờ)')
ac = autocorrs(s.asfreq('h'), [1,2,24,168]); print(ac); SUMMARY['acf'] = ac
print(f"Nhận xét: tự tương quan lag1={ac['lag1']}, lag24={ac['lag24']}, lag168={ac['lag168']} → mùa ngày và tuần rõ; đặc trưng lag 24/168 hữu ích.")"""),
(M, "## 8. Kiểm định dừng (ADF / KPSS)\nADF: H0 = không dừng. KPSS: H0 = dừng. p-value của KPSS bị statsmodels chặn trong [0.01, 0.1]."),
(C, """res = pd.DataFrame([stationarity(sh, 'cnt giờ'), stationarity(sd, 'cnt ngày'), stationarity(sd.diff(), 'cnt ngày, sai phân 1')]); display(res)
SUMMARY['stationarity'] = res.set_index('series')['kết luận'].to_dict()"""),
(C, """print('Nhận xét:', '; '.join(f"{r.series}: ADF p={r.ADF_p}, KPSS p={r['KPSS_p(bị chặn 0.01-0.1)']} → {r['kết luận']}" for _, r in res.iterrows()))"""),
(M, "## 9. Tương quan với biến ngoại sinh"),
(C, """ex = ['temp','atemp','hum','windspeed','hr','weekday','workingday','holiday','weathersit','season','yr']
corr = df[ex+['cnt']].corr(method='spearman')
plt.figure(figsize=(8,6)); sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, annot_kws={'size':7}); plt.show()
c = corr['cnt'].drop('cnt').sort_values(key=abs, ascending=False); display(c.round(3))
print('Tương quan temp–atemp:', round(df.temp.corr(df.atemp),3))
SUMMARY['top_exog'] = c.round(3).head(3).to_dict()"""),
(C, """print(f"Nhận xét: biến tương quan (Spearman) mạnh nhất với cnt: {', '.join(f'{k}={v:.2f}' for k,v in c.head(4).items())}. "
      f"temp và atemp gần trùng (r={df.temp.corr(df.atemp):.3f}) → giữ một. Thời tiết là biến quan sát cùng thời điểm: khi dự báo nhiều bước cần dùng dự báo thời tiết hoặc lag.")"""),
(C, SAVE),
])

# ---------------------------------------------------------------- TETOUAN
build("eda_02_tetouan_power.ipynb", [
(M, """# EDA 2 — Power Consumption of Tetouan City (UCI 849)
**Nguồn:** https://archive.ics.uci.edu/dataset/849 · **License:** CC BY 4.0 · **Paper gốc:** Salam & El Hibaoui (2018), *Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city*, IEEE IRSEC, DOI 10.1109/IRSEC.2018.8703007.
Chuỗi phụ tải điện của ba vùng phân phối tại Tetouan, Morocco, ghi nhận mỗi 10 phút trong năm 2017, kèm nhiệt độ, độ ẩm, tốc độ gió và bức xạ. Mục tiêu: dự báo `Zone 1`, `Zone 2`, `Zone 3`.
> Cách đọc: mỗi phần có ô code, rồi ô **Nhận xét** in ra từ chính số liệu vừa tính."""),
(C, SETUP),
(M, "## 1. Đọc dữ liệu, shape, kiểu"),
(C, """df = pd.read_csv(RAW/'Tetuan City power consumption.csv')
df['t'] = pd.to_datetime(df['DateTime'])
df = df.rename(columns={
    'Zone 1 Power Consumption': 'zone1',
    'Zone 2  Power Consumption': 'zone2',
    'Zone 3  Power Consumption': 'zone3',
})
targets = ['zone1', 'zone2', 'zone3']
exog = ['Temperature', 'Humidity', 'Wind Speed', 'general diffuse flows', 'diffuse flows']
print('shape:', df.shape); display(df.head(3)); display(overview(df))
SUMMARY.update(dataset='tetouan', rows=len(df), cols=df.shape[1]-1, freq='10 phút', n_series=3,
               target='zone1, zone2, zone3')"""),
(M, "## 2. Khoảng thời gian, lưới thời gian, missing và trùng"),
(C, """g, missing = time_gaps(df['t'], '10min'); display(pd.Series(g))
print('Dòng trùng hoàn toàn:', df.duplicated().sum(), '| NA tổng:', df.isna().sum().sum())
SUMMARY.update(start=g['start'], end=g['end'], missing_steps=g['n_missing_steps'], dup_ts=g['n_duplicated_ts'], n_na=int(df.isna().sum().sum()))"""),
(C, """print(f"Nhận xét: có {g['n_expected']} mốc 10 phút kỳ vọng, thiếu {g['n_missing_steps']} mốc và có {g['n_duplicated_ts']} timestamp trùng. "
      f"Dữ liệu có {df.isna().sum().sum()} NA trong ô. Đây là lưới thời gian sạch, thuận lợi cho tạo cửa sổ DL và đánh giá multi-step.")"""),
(M, "## 3. Thống kê mô tả và phân phối target"),
(C, """num = targets + exog
st = shape_stats(df[num]); display(st)
plot_dists(df, targets)
SUMMARY['target_summary'] = st.loc[targets, ['mean','50%','std','min','max','skew','kurtosis']].to_dict('index')
SUMMARY['target_mean'] = round(float(st.loc['zone1', 'mean']), 3)
SUMMARY['target_skew'] = round(float(st.loc['zone1', 'skew']), 3)
SUMMARY['target_kurt'] = round(float(st.loc['zone1', 'kurtosis']), 3)
SUMMARY['target_cv'] = round(float(st.loc['zone1', 'std'] / st.loc['zone1', 'mean']), 3)
print('Skew log1p:', {c: round(np.log1p(df[c]).skew(), 3) for c in targets})"""),
(C, """print('Nhận xét: ba vùng có quy mô và phân phối khác nhau; cần scale từng target hoặc dùng loss có trọng số nếu huấn luyện multi-output. '
      'Kiểm tra log1p trước khi dùng nếu muốn giảm ảnh hưởng của các đỉnh phụ tải.')"""),
(M, "## 4. Outlier theo IQR"),
(C, """out = iqr_outliers(df[targets]); display(out)
SUMMARY['target_outlier_pct'] = float(out.loc['zone1', 'pct'])
print('Nhận xét: các điểm vượt IQR có thể là giờ cao điểm thật. Không nên xoá tự động; cần đối chiếu theo thời gian và đánh giá thêm bằng loss bền vững.')"""),
(M, "## 5. Xu hướng, mùa vụ và tương quan giữa ba vùng"),
(C, """hourly = df.set_index('t')[targets].resample('h').mean()
fig, ax = plt.subplots(3, 1, figsize=(12, 8))
hourly.resample('D').mean().plot(ax=ax[0], title='Phụ tải trung bình ngày')
hourly.groupby(hourly.index.hour).mean().plot(ax=ax[1], title='Phụ tải trung bình theo giờ')
hourly.groupby(hourly.index.dayofweek).mean().plot(ax=ax[2], title='Phụ tải trung bình theo thứ trong tuần')
plt.tight_layout(); plt.show()
monthly = hourly.groupby(hourly.index.month).mean(); print('TB theo tháng:'); display(monthly.round(1))
print('Tương quan Pearson giữa các target:'); display(df[targets].corr().round(3))"""),
(C, """stl = stl_strength(hourly['zone1'], period=24, title='STL Zone 1 sau khi lấy trung bình theo giờ')
SUMMARY.update(trend_strength=stl['trend_strength'], seasonal_strength=stl['seasonal_strength'])
print(f"Nhận xét: sau khi quy về giờ, Zone 1 có độ mạnh mùa vụ ngày STL={stl['seasonal_strength']} và độ mạnh xu hướng={stl['trend_strength']}. "
      'Nên kiểm tra thêm mùa vụ tuần và sự khác nhau giữa các vùng trước khi chọn window length.')"""),
(M, "## 6. ACF/PACF và kiểm định dừng"),
(C, """s = hourly['zone1']
acf_pacf(s, lags=200, title='Zone 1 (trung bình theo giờ)')
ac = autocorrs(s, [1, 3, 6, 24, 168]); print(ac); SUMMARY['acf'] = ac
res = pd.DataFrame([stationarity(s, 'Zone 1 theo giờ')]); display(res)
SUMMARY['stationarity'] = res.set_index('series')['kết luận'].to_dict()
print(f"Nhận xét: ACF lag1={ac['lag1']}, lag24={ac['lag24']}, lag168={ac['lag168']}; lag 24 và 168 giúp kiểm tra mùa ngày/tuần. "
      'Kết quả ADF/KPSS chỉ là chẩn đoán; mô hình DL vẫn cần validation theo thời gian.')"""),
(M, "## 7. Tương quan với biến ngoại sinh"),
(C, """corr = df[targets + exog].corr(method='spearman')
plt.figure(figsize=(10, 7)); sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, annot_kws={'size':7}); plt.show()
c = corr['zone1'].drop(targets).sort_values(key=abs, ascending=False); display(c.round(3))
SUMMARY['top_exog'] = c.round(3).head(3).to_dict()
print(f"Nhận xét: các ngoại sinh liên quan Zone 1 mạnh nhất theo Spearman: {', '.join(f'{k}={v:.2f}' for k,v in c.head(3).items())}. "
      'Khi dự báo nhiều bước, chỉ dùng ngoại sinh thực sự có sẵn hoặc dùng giá trị dự báo/lag của chúng.')"""),
(C, SAVE),
])
# ---------------------------------------------------------------- COMPARE
build("eda_03_so_sanh_va_tien_xu_ly.ipynb", [
(M, """# EDA 3 — So sánh 2 bộ và gợi ý tiền xử lý
Đọc `reports/summary_*.json` do hai notebook trước sinh ra (chạy 01–02 trước)."""),
(C, SETUP.replace("SUMMARY = {}  # các số chính, lưu ra reports/ để notebook so sánh dùng lại", "import json")),
(C, """S = {k: json.load(open(ROOT/'reports'/f'summary_{k}.json')) for k in ['bike','tetouan']}
rows = {
    'bike': {
        'license': 'CC BY 4.0', 'mục tiêu': 'cnt', 'ngoại sinh': 'thời tiết, lịch',
        'freq': S['bike']['freq'], 'rows': S['bike']['rows'], 'n_series': S['bike']['n_series'],
        'missing_steps': S['bike']['missing_steps'], 'n_na': S['bike']['n_na'],
        'seasonal_strength': S['bike'].get('seasonal_strength'), 'target_mean': S['bike'].get('target_mean'),
    },
    'tetouan': {
        'license': 'CC BY 4.0', 'mục tiêu': 'zone1, zone2, zone3', 'ngoại sinh': 'thời tiết, bức xạ',
        'freq': S['tetouan']['freq'], 'rows': S['tetouan']['rows'], 'n_series': S['tetouan']['n_series'],
        'missing_steps': S['tetouan']['missing_steps'], 'n_na': S['tetouan']['n_na'],
        'seasonal_strength': S['tetouan'].get('seasonal_strength'), 'target_mean': S['tetouan'].get('target_mean'),
    },
}
display(pd.DataFrame(rows).T)
for k in S: print(k, 'ACF:', S[k].get('acf'), '| dừng:', S[k].get('stationarity'))"""),
(M, """## Gợi ý tiền xử lý

- **Bike:** bỏ `casual`, `registered` và `instant`; giữ một trong `temp`/`atemp`; dựng lưới giờ đều; log1p nếu cần; tạo lag 24/168; chia theo thời gian.
- **Tetouan:** parse `DateTime`; chuẩn hoá tên ba target; scale từng target; tạo hour/day-of-week/month; quyết định giữ tần suất 10 phút hay resample theo giờ; dùng multi-output loss nếu dự báo ba zone đồng thời.
- **Chung:** fit scaler/imputer trên train; không random split; báo cáo naive và seasonal-naive; ghi rõ forecast horizon và quy tắc resample.
"""),
])
