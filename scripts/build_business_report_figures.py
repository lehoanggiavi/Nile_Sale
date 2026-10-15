"""Đối chiếu số báo cáo với CSV đã duyệt và vẽ hai hình; không ghi nguồn/model."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/phase6'
SOURCE = ROOT / 'data/processed/nile_sales_clean.csv'


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == 'e009438801cee5c8f4c848b523380a14cec3464beffb79ea6703395ee2f96829'
    df = pd.read_csv(SOURCE, parse_dates=['Sales_Date', 'Delivery_Date'])
    df['month'] = df['Sales_Date'].dt.strftime('%Y-%m')
    month = df.groupby('month').agg(rows=('Qty', 'size'), qty=('Qty', 'sum'), value=('Line_Amount', 'sum'))
    prior = pd.read_csv(ROOT / 'reports/phase4b/monthly.csv').set_index('ym')
    pd.testing.assert_frame_equal(month, prior[['rows', 'qty', 'value']], check_names=False)
    assert month['value'].pct_change().idxmax() == '2025-07'
    assert df['SKU_Code'].nunique() == 50 and df['To_Location'].nunique() == 28
    category = df.groupby('Category')['Line_Amount'].sum()
    published = pd.read_csv(ROOT / 'reports/phase4b/contrib_category.csv').set_index('Category')['value']
    pd.testing.assert_series_equal(category, published, check_names=False)
    june, july = month.loc['2025-06'], month.loc['2025-07']
    by_month = df.groupby(['month', 'Category'])['Line_Amount'].sum()
    delta = (by_month.loc['2025-07'] - by_month.loc['2025-06']).sort_values(ascending=False)
    assert delta.sum() == july['value'] - june['value'] == 322833
    published = pd.read_csv(ROOT / 'reports/phase4b/t7_decomp.csv').set_index('Category')['delta'].sort_index()
    pd.testing.assert_series_equal(delta.sort_index(), published, check_names=False)
    two = df[df['SKU_Code'].isin(['BPC-1041', 'BPC-1048']) & df['month'].isin(['2025-06', '2025-07'])]
    sku = two.groupby(['SKU_Code', 'month']).agg(qty=('Qty', 'sum'), value=('Line_Amount', 'sum'))
    sku_delta = int(sku.xs('2025-07', level='month')['value'].sum() - sku.xs('2025-06', level='month')['value'].sum())
    assert sku_delta == 94461
    assert (df[df['SKU_Code'].isin(['BPC-1041', 'BPC-1048'])].groupby('SKU_Code')['month'].nunique() == 7).all()
    valid_flag = df['Is_Returned'].isin([0, 1])
    flags = df[valid_flag].groupby('month')['Is_Returned'].agg(['size', 'sum'])
    assert int(flags['size'].sum()) == 9705 and int(flags['sum'].sum()) == 574
    gap = (df['Delivery_Date'] - df['Sales_Date']).dt.days
    assert gap.notna().all() and (gap >= 0).all() and gap.median() == 3
    distribution = gap.value_counts().sort_index()
    published = pd.read_csv(ROOT / 'reports/phase4b/leadtime_dist.csv').set_index('gap_ngay')['so_dong']
    pd.testing.assert_series_equal(distribution, published, check_names=False)
    assert distribution.loc[[2, 3]].sum() == 5393 and category.sum() == 8787091
    kolkata = df[df['To_Location'] == 'Kolkata'].copy()
    kolkata['gap'] = gap.loc[kolkata.index]
    routes = kolkata.groupby('From_Location')['gap'].agg(['size', 'median'])
    assert routes['size'].to_dict() == {'Gurgaon': 273, 'Hyderabad': 217, 'Navi Mumbai': 237}
    assert (routes['median'] == 5).all()

    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'Segoe UI', 'font.size': 10, 'figure.dpi': 160})
    fig, ax = plt.subplots(figsize=(10, 4.5))
    labels = ['Tháng 6'] + list(delta.index) + ['Tháng 7']
    running = int(june['value'])
    ax.bar(0, running, color='#ECE6FF', edgecolor='#865EFF')
    ax.text(0, running + 20000, f'{running:,}'.replace(',', '.'), ha='center', fontsize=9)
    for i, (name, amount) in enumerate(delta.items(), 1):
        amount = int(amount)
        ax.plot([i - 0.6, i + 0.6], [running, running], color='#BBB7C7', linewidth=0.8)
        ax.bar(i, abs(amount), bottom=min(running, running + amount), color='#865EFF' if amount >= 0 else '#E66C37')
        running += amount
        ax.text(i, max(running, running - amount) + 20000,
                f'{amount:+,}'.replace(',', '.'), ha='center', fontsize=9)
    assert running == int(july['value']), 'Waterfall does not reconcile to July'
    ax.bar(6, running, color='#6B007B')
    ax.text(6, running + 20000, f'{running:,}'.replace(',', '.'), ha='center', fontsize=9)
    ax.set(xticks=range(7), xticklabels=labels, ylim=(0, 2000000),
           ylabel='Giá trị dòng nguồn (triệu; chưa xác nhận tiền tệ)',
           title='Tháng 7 tăng 322.833 — Makeup đóng góp 159.095')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f'{value / 1e6:.1f}'))
    ax.spines[['top', 'right']].set_visible(False)
    fig.text(0.08, 0.01, 'Bán tháng 6–7/2025 · Tổng tháng 6/7: 1.597/1.722 dòng · Màu cam: phần giảm', fontsize=8)
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(OUT / 'july_change.png'); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax.bar(distribution.index, distribution.values, color='#865EFF', width=0.65)
    for days, count in distribution.items():
        ax.text(days, count + 45, f'{count:,}'.replace(',', '.'), ha='center', fontsize=10)
    ax.set(xticks=distribution.index, xlabel='Hiệu ngày giao − ngày bán ghi trong file (ngày)',
           ylabel='Số dòng nguồn', ylim=(0, 3200),
           title='5.393/9.705 dòng có hiệu ngày 2–3 ngày (55,57%)')
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT / 'source_day_gap.png'); plt.close(fig)

    metrics = {'sourceSha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'monthly': month.reset_index().to_dict('records'), 'categories': category.to_dict(),
        'julyDelta': delta.to_dict(), 'twoSku': sku.reset_index().to_dict('records'),
        'twoSkuIncrease': sku_delta, 'twoSkuContributionToJulyIncrease': sku_delta / 322833,
        'julyValueChange': float(july['value'] / june['value'] - 1),
        'julyQtyChange': float(july['qty'] / june['qty'] - 1),
        'julyValuePerDayChange': float((july['value'] / 31) / (june['value'] / 30) - 1),
        'flagMonthly': flags.reset_index().to_dict('records'), 'dayDistribution': distribution.to_dict(),
        'kolkataRoutes': routes.reset_index().to_dict('records'),
        'days2or3Share': 5393 / 9705, 'checksPassed': True}
    path = ROOT / 'Log/phase6/evidence/run.json'
    run = json.loads(path.read_text(encoding='utf-8-sig')); run['reportNumbers'] = metrics
    path.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Source, published tables, waterfall, flags and day distribution matched; two figures written')


if __name__ == '__main__':
    main()
