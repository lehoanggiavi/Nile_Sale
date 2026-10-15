"""Phase 4B: 4 cau hoi tren CSV sach. Doc CSV -> bang + hinh + assert tong."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CSV = "data/processed/nile_sales_clean.csv"
OUT = "reports/phase4b"
plt.rcParams.update({"font.size": 10, "figure.dpi": 120})

df = pd.read_csv(CSV)
df["Sales_Date"] = pd.to_datetime(df["Sales_Date"])
df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"])
df["gap"] = (df["Delivery_Date"] - df["Sales_Date"]).dt.days
df["ym"] = df["Sales_Date"].dt.strftime("%Y-%m")

TOT = {"rows": 9705, "qty": 13087, "value": 8787091, "codes": 6246,
       "flag1": 574, "flagN": 9705, "dayN": 9705, "median": 3}
assert len(df) == TOT["rows"]
assert df["Qty"].sum() == TOT["qty"]
assert df["Line_Amount"].sum() == TOT["value"]
assert df["Order_ID"].nunique() == TOT["codes"]
assert (df["Is_Returned"] == 1).sum() == TOT["flag1"]
assert df["gap"].median() == TOT["median"]
assert df["Is_Returned"].isin([0, 1]).sum() == TOT["flagN"]
assert ((df["Sales_Date"].notna()) & (df["Delivery_Date"].notna())
        & (df["Delivery_Date"] >= df["Sales_Date"])).sum() == TOT["dayN"]

# --- Q1: thang ---
m = df.groupby("ym").agg(rows=("Qty", "size"), qty=("Qty", "sum"),
                         value=("Line_Amount", "sum")).reset_index()
m["prev"] = m["value"].shift(1)
m["chg"] = (m["value"] - m["prev"]) / m["prev"]
m.to_csv(f"{OUT}/monthly.csv", index=False)
mc = df.groupby(["ym", "Category"]).agg(rows=("Qty", "size"), qty=("Qty", "sum"),
                                        value=("Line_Amount", "sum")).reset_index()
mc.to_csv(f"{OUT}/month_category.csv", index=False)
t7 = mc[mc["ym"] == "2025-07"].merge(mc[mc["ym"] == "2025-06"][["Category", "value"]],
                                       on="Category", suffixes=("", "_prev"))
t7["delta"] = t7["value"] - t7["value_prev"]
t7[["Category", "value_prev", "value", "delta"]].to_csv(f"{OUT}/t7_decomp.csv", index=False)
assert t7["delta"].sum() == m.loc[m["ym"] == "2025-07", "value"].iloc[0] - m.loc[m["ym"] == "2025-06", "value"].iloc[0]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.bar(m["ym"], m["value"] / 1e6, color="#4C78A8")
ax1.set_ylabel("Giá trị nguồn (triệu)")
ax1.set_title("Giá trị nguồn theo tháng 1–7/2025 (9.705 dòng, tổng 8.787.091)")
ax2.bar(m["ym"], m["qty"], color="#54A24B")
ax2.set_ylabel("Lượng bán nguồn (Qty, tổng 13.087)")
ax2.set_xlabel("Tháng bán (năm 2025)")
for x, v, q in zip(m["ym"], m["value"], m["qty"]):
    ax1.text(x, v / 1e6, f" {v/1e6:.2f}", va="bottom", fontsize=8)
fig.tight_layout()
fig.savefig(f"{OUT}/trend_month.png")
plt.close(fig)

# --- Q2: dong gop ---
cat = df.groupby("Category").agg(rows=("Qty", "size"), qty=("Qty", "sum"),
                                 value=("Line_Amount", "sum"),
                                 sku=("SKU_Code", "nunique")).reset_index()
cat["share"] = cat["value"] / cat["value"].sum()
cat.to_csv(f"{OUT}/contrib_category.csv", index=False)
assert abs(cat["share"].sum() - 1) < 1e-9
sku_all = df.groupby(["Category", "SKU_Code"]).agg(rows=("Qty", "size"),
                                                       qty=("Qty", "sum"),
                                                       value=("Line_Amount", "sum")).reset_index()
sku_all["share"] = sku_all["value"] / df["Line_Amount"].sum()
assert len(sku_all) == 50
sku_all.sort_values("value", ascending=False).to_csv(f"{OUT}/sku_all.csv", index=False)
sku_all.sort_values("value", ascending=False).head(15).to_csv(f"{OUT}/sku_top15.csv", index=False)
jj = df[df["ym"].isin(["2025-06", "2025-07"])].groupby(
    ["Category", "SKU_Code", "ym"]).agg(rows=("Qty", "size"), qty=("Qty", "sum"),
                                       value=("Line_Amount", "sum")).reset_index()
jj = jj.pivot_table(index=["Category", "SKU_Code"], columns="ym",
                    values=["rows", "qty", "value"]).fillna(0).astype(int)
jj.columns = ["_".join(c) for c in jj.columns]
jj = jj.reset_index()
for c in ["rows", "qty", "value"]:
    jj[f"d_{c}"] = jj[f"{c}_2025-07"] - jj[f"{c}_2025-06"]
jj.sort_values("d_value", ascending=False).to_csv(f"{OUT}/sku_jun_jul.csv", index=False)
dest = df.groupby("To_Location").agg(rows=("Qty", "size"), qty=("Qty", "sum"),
                                     value=("Line_Amount", "sum")).reset_index()
dest["share"] = dest["value"] / dest["value"].sum()
dest.to_csv(f"{OUT}/destination.csv", index=False)
ct = df.groupby(["Category", "City_Tier"]).agg(rows=("Qty", "size"),
                                               value=("Line_Amount", "sum")).reset_index()
ct["share"] = ct["value"] / df["Line_Amount"].sum()
ct.to_csv(f"{OUT}/combo_cat_tier.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 4.5))
o = cat.sort_values("value", ascending=True)
ax.barh(o["Category"], o["value"] / 1e6, color="#54A24B")
for _, r in o.iterrows():
    ax.text(r["value"] / 1e6, r["Category"], f" {r['share']:.1%}", va="center")
ax.set_xlabel("Giá trị nguồn (triệu, tổng 8.787.091)")
ax.set_xlim(0, 2.9)
ax.set_title("Đóng góp giá trị theo Category (5 nhóm, năm 2025)")
fig.tight_layout()
fig.savefig(f"{OUT}/contrib_category.png")
plt.close(fig)

# --- Q3: co ---
for key, fn in [("returns_month.csv", ["ym"]), ("returns_category.csv", ["Category"]),
                ("returns_location.csv", ["To_Location"])]:
    g = df.groupby(fn).agg(n=("Is_Returned", "size"),
                           n1=("Is_Returned", lambda s: (s == 1).sum())).reset_index()
    g["rate"] = g["n1"] / g["n"]
    g.to_csv(f"{OUT}/{key}", index=False)

fig, ax = plt.subplots(figsize=(8, 4.5))
o = cat.merge(df.groupby("Category")["Is_Returned"].agg(n1=lambda s: (s == 1).sum(),
                                                       n="size"),
              on="Category")
o["rate"] = o["n1"] / o["n"]
o = o.sort_values("rate", ascending=True)
ax.barh(o["Category"], o["rate"] * 100, color="#EECA3B")
for _, r in o.iterrows():
    ax.text(r["rate"] * 100, r["Category"], f"  {r['n1']}/{r['n']} ({r['rate']:.2%})",
            va="center")
ax.set_xlabel("Tỷ lệ dòng cờ 1 (%) kèm tử số/mẫu số)")
ax.set_xlim(0, 6.6)
ax.set_title("Tỷ lệ cờ theo Category (tử/mẫu tính lại từng nhóm)")
fig.tight_layout()
fig.savefig(f"{OUT}/returns_category.png")
plt.close(fig)

# --- Q4: hieu ngay ---
d = df["gap"].value_counts().sort_index().reset_index()
d.columns = ["gap_ngay", "so_dong"]
d.to_csv(f"{OUT}/leadtime_dist.csv", index=False)
for key, col in [("leadtime_location.csv", "To_Location"), ("leadtime_from.csv", "From_Location"),
                 ("leadtime_category.csv", "Category"), ("leadtime_tier.csv", "City_Tier")]:
    g = df.groupby(col)["gap"].agg(n="size", median="median").reset_index()
    g.to_csv(f"{OUT}/{key}", index=False)
r = df.groupby(["From_Location", "To_Location"])["gap"].agg(n="size",
                                                            median="median").reset_index()
r.to_csv(f"{OUT}/leadtime_from_to.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(d["gap_ngay"], d["so_dong"], color="#79706E")
ax.set_xlabel("Hiệu ngày giao - bán (ngày, theo từng dòng)")
ax.set_ylabel("Số dòng (tổng 9.705, năm 2025)")
ax.set_title("Phân phối hiệu ngày (trung vị 3 ngày)")
fig.tight_layout()
fig.savefig(f"{OUT}/leadtime_hist.png")
plt.close(fig)

print("OK totals:", TOT)
print("T7 MoM delta:", int(t7["delta"].sum()), "| top cat:", t7.sort_values("delta", ascending=False)[["Category", "delta"]].head(3).to_dict("records"))
print("Kolkata/Bengaluru median:", df[df.To_Location == "Kolkata"]["gap"].median(),
      df[df.To_Location == "Bengaluru"]["gap"].median())
