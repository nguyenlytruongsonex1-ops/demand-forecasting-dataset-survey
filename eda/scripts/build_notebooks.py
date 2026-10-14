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

# ---------------------------------------------------------------- PM2.5
build("eda_02_beijing_pm25.ipynb", [
(M, """# EDA 2 — Beijing PM2.5 (UCI 381)
**Nguồn:** https://archive.ics.uci.edu/dataset/381 · **License:** CC BY 4.0 · **Paper gốc:** Liang et al. (2015), *Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and winter heating*, Proc. Royal Society A 471:20150257, DOI 10.1098/rspa.2015.0257.

Nồng độ PM2.5 theo giờ tại Đại sứ quán Mỹ ở Bắc Kinh, 2010–2014, kèm khí tượng (DEWP điểm sương, TEMP, PRES, cbwd hướng gió, Iws tốc độ gió cộng dồn, Is/Ir số giờ tuyết/mưa cộng dồn). Mục tiêu: `pm2.5`."""),
(C, SETUP),
(M, "## 1. Đọc dữ liệu, shape, kiểu"),
(C, """df = pd.read_csv(RAW/'PRSA_data_2010.1.1-2014.12.31.csv')
df['t'] = pd.to_datetime(df[['year','month','day','hour']]); df = df.rename(columns={'pm2.5':'pm25'})
print('shape:', df.shape); display(df.head(3)); display(overview(df))
SUMMARY.update(dataset='pm25', rows=len(df), cols=df.shape[1]-1, freq='giờ', n_series=1)"""),
(M, "## 2. Khoảng thời gian, giá trị thiếu, trùng lặp"),
(C, """g, missing = time_gaps(df['t'], 'h'); display(pd.Series(g))
na = df.pm25.isna(); runs = na.ne(na.shift()).cumsum()[na].value_counts()
print(f'pm25 thiếu: {na.sum()} ({na.mean()*100:.2f}%) | số đoạn thiếu liên tiếp: {len(runs)} | đoạn dài nhất: {runs.max()} giờ')
print('Phân bố độ dài đoạn thiếu:'); display(runs.describe().round(1))
print('Thiếu theo năm:', df[na].year.value_counts().sort_index().to_dict())
SUMMARY.update(start=g['start'], end=g['end'], missing_steps=g['n_missing_steps'], dup_ts=g['n_duplicated_ts'], n_na=int(na.sum()))"""),
(C, """print(f"Nhận xét: lưới giờ đầy đủ ({g['n_missing_steps']} giờ thiếu, {g['n_duplicated_ts']} trùng) nhưng mục tiêu pm25 thiếu {na.sum()} giá trị ({na.mean()*100:.2f}%), "
      f"chia thành {len(runs)} đoạn, dài nhất {runs.max()} giờ, trung vị {runs.median():.0f} giờ. Đoạn ngắn có thể nội suy; đoạn dài nên che (mask) khi tính loss/đánh giá thay vì nội suy. "
      f"Năm 2010 có {int((df[na].year==2010).sum())} giá trị thiếu, 24 giờ đầu toàn NA: {df.pm25.iloc[:24].isna().all()}.")"""),
(M, "## 3. Thống kê mô tả, phân phối, độ lệch"),
(C, """num = ['pm25','DEWP','TEMP','PRES','Iws','Is','Ir']
st = shape_stats(df[num]); display(st); plot_dists(df, num)
display(df.cbwd.value_counts())
SUMMARY.update(target_mean=st.loc['pm25','mean'], target_skew=st.loc['pm25','skew'], target_kurt=st.loc['pm25','kurtosis'], target_cv=round(st.loc['pm25','std']/st.loc['pm25','mean'],3))
print('skew log1p(pm25):', round(np.log1p(df.pm25).skew(),3), '| % giờ Is>0:', round((df.Is>0).mean()*100,2), '| % giờ Ir>0:', round((df.Ir>0).mean()*100,2))"""),
(C, """print(f"Nhận xét: pm25 TB {st.loc['pm25','mean']:.1f}, trung vị {st.loc['pm25','50%']:.0f}, max {st.loc['pm25','max']:.0f} µg/m³; "
      f"skew={st.loc['pm25','skew']:.2f}, kurtosis={st.loc['pm25','kurtosis']:.2f} → lệch phải nặng; log1p cho skew {np.log1p(df.pm25).skew():.2f}. "
      f"Iws skew={st.loc['Iws','skew']:.2f}; Is/Ir gần như toàn 0 (Is>0 {(df.Is>0).mean()*100:.2f}%, Ir>0 {(df.Ir>0).mean()*100:.2f}% số giờ) → biến thưa.")"""),
(M, "## 4. Outlier (IQR 1.5)"),
(C, """out = iqr_outliers(df[num]); display(out); SUMMARY['target_outlier_pct'] = out.loc['pm25','pct']
print(f"Nhận xét: {int(out.loc['pm25','n_outliers'])} giờ ({out.loc['pm25','pct']}%) pm25 > {out.loc['pm25','upper']:.0f}; đây là các đợt ô nhiễm thật (giá trị quan trọng nhất cần dự báo) → không xoá; dùng log hoặc loss bền vững.")"""),
(M, "## 5. Xu hướng & mùa vụ"),
(C, """s = df.set_index('t')['pm25']
fig, ax = plt.subplots(3,1, figsize=(12,8))
s.resample('D').mean().plot(ax=ax[0], lw=.6, title='TB ngày'); s.resample('MS').mean().plot(ax=ax[0], lw=2)
df.groupby('month').pm25.mean().plot.bar(ax=ax[1], title='TB theo tháng'); df.groupby('hour').pm25.mean().plot(ax=ax[2], title='TB theo giờ trong ngày')
plt.tight_layout(); plt.show()
yr = df.groupby('year').pm25.mean().round(1); mo = df.groupby('month').pm25.mean(); hr = df.groupby('hour').pm25.mean()
print('TB theo năm:', yr.to_dict())"""),
(C, """sd = s.resample('D').mean().interpolate()
sw = stl_strength(sd, period=7, title='STL TB ngày (period=7)')
sh = s.interpolate(limit_direction='both')
sday = stl_strength(sh, period=24, plot=False)
print('STL ngày (period 7):', sw, '| STL giờ (period 24):', sday)
SUMMARY.update(trend_strength=sw['trend_strength'], seasonal_strength=sday['seasonal_strength'])"""),
(C, """print(f"Nhận xét: TB theo năm {yr.to_dict()} → không có xu hướng đơn điệu mạnh. Tháng cao nhất {mo.idxmax()} ({mo.max():.0f}), thấp nhất {mo.idxmin()} ({mo.min():.0f}) → mùa đông (sưởi) ô nhiễm hơn. "
      f"Theo giờ: cao nhất {hr.idxmax()}h ({hr.max():.0f}), thấp nhất {hr.idxmin()}h ({hr.min():.0f}). Độ mạnh mùa ngày STL = {sday['seasonal_strength']} (mức vừa); STL chuỗi ngày period 7 = {sw} → gần như không có mùa vụ tuần, biến động chủ yếu theo đợt thời tiết.")"""),
(M, "## 6. ACF/PACF"),
(C, """acf_pacf(sh, lags=100, title='pm25 (giờ, đã nội suy cho vẽ)')
ac = autocorrs(s, [1,2,6,24,168]); print(ac); SUMMARY['acf'] = ac
print(f"Nhận xét: lag1={ac['lag1']} rất cao nhưng giảm nhanh (lag24={ac['lag24']}, lag168={ac['lag168']}) → chuỗi có quán tính ngắn hạn, dự báo xa sẽ khó; PACF gợi ý vài lag đầu là chính.")"""),
(M, "## 7. Kiểm định dừng"),
(C, """res = pd.DataFrame([stationarity(s.dropna(), 'pm25 giờ (bỏ NA)'), stationarity(sd, 'pm25 TB ngày')]); display(res)
SUMMARY['stationarity'] = res.set_index('series')['kết luận'].to_dict()
print('Nhận xét:', '; '.join(f"{r.series}: ADF p={r.ADF_p}, KPSS p={r['KPSS_p(bị chặn 0.01-0.1)']} → {r['kết luận']}" for _, r in res.iterrows()))"""),
(M, "## 8. Tương quan với biến ngoại sinh"),
(C, """d2 = pd.get_dummies(df[['pm25','DEWP','TEMP','PRES','Iws','Is','Ir','cbwd']], columns=['cbwd'], dtype=float)
corr = d2.corr(method='spearman'); plt.figure(figsize=(8,6)); sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, annot_kws={'size':7}); plt.show()
c = corr['pm25'].drop('pm25').sort_values(key=abs, ascending=False); display(c.round(3))
display(df.groupby('cbwd').pm25.agg(['mean','median','count']).round(1))
SUMMARY['top_exog'] = c.round(3).head(3).to_dict()"""),
(C, """bw = df.groupby('cbwd').pm25.mean()
print(f"Nhận xét: tương quan Spearman mạnh nhất với pm25: {', '.join(f'{k}={v:.2f}' for k,v in c.head(4).items())}. "
      f"Hướng gió quan trọng: TB pm25 khi gió {bw.idxmax()} là {bw.max():.0f}, khi gió {bw.idxmin()} là {bw.min():.0f}. Iws là tốc độ gió CỘNG DỒN (reset khi đổi hướng) → cân nhắc sai phân.")"""),
(C, SAVE),
])

# ---------------------------------------------------------------- Compare
build("eda_03_so_sanh_va_tien_xu_ly.ipynb", [
(M, """# EDA 3 — So sánh 2 bộ và gợi ý tiền xử lý
Đọc `reports/summary_*.json` do 2 notebook trước sinh ra (chạy 01–02 trước)."""),
(C, SETUP.replace("SUMMARY = {}  # các số chính, lưu ra reports/ để notebook so sánh dùng lại", "import json")),
(C, """S = {k: json.load(open(ROOT/'reports'/f'summary_{k}.json')) for k in ['bike','pm25']}
cols = ['rows','n_series','freq','start','end','missing_steps','dup_ts','n_na','target_mean','target_cv','target_skew','target_kurt','target_outlier_pct','trend_strength','seasonal_strength']
tab = pd.DataFrame(S).T[cols]
tab.insert(0, 'license', ['CC BY 4.0','CC BY 4.0'])
tab.insert(1, 'mục tiêu', ['cnt','pm2.5'])
tab.insert(2, 'ngoại sinh', ['thời tiết, lịch','khí tượng, hướng gió'])
display(tab)
for k in S: print(k, 'ACF:', S[k]['acf'], '| dừng:', S[k]['stationarity'])"""),
(M, """## Gợi ý tiền xử lý (dựa trên kết quả ở trên)

| Bộ | Gợi ý |
|---|---|
| **Bike** | Bỏ `casual`, `registered` (rò rỉ mục tiêu), `instant`; giữ một trong `temp`/`atemp`. Dựng lưới giờ đều, quyết định điền giờ thiếu (0 hoặc nội suy) và đánh dấu bằng cờ. Biến đổi log1p mục tiêu (lệch phải). Chia train/test theo thời gian; chú ý tăng trưởng giữa 2011→2012 (drift) — cân nhắc đặc trưng xu hướng hoặc chuẩn hoá theo cửa sổ. Đặc trưng: giờ, thứ, workingday, lag 24/168. |
| **PM2.5** | Mục tiêu thiếu theo đoạn: nội suy đoạn ngắn, mask đoạn dài khi tính loss/metric; bỏ 24 giờ đầu toàn NA. log1p mục tiêu (lệch phải nặng). One-hot `cbwd`; `Iws/Is/Ir` là cộng dồn → cân nhắc sai phân. Đỉnh ô nhiễm là tín hiệu thật, không xoá outlier. |
| **Chung** | Chia theo thời gian (không xáo trộn), fit scaler/imputer chỉ trên train, luôn báo cáo baseline naive và seasonal naive. |
"""),
])
print("built")
