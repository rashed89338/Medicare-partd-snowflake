"""Create local PNG charts from exported Snowflake analysis CSVs.
Usage: python scripts/make_charts.py .
The 2024 concentration chart requires results/a5_concentration_2024.csv.
"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

project = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
results, charts = project / "results", project / "charts"
charts.mkdir(parents=True, exist_ok=True)

def finish(name, title, xlabel="", ylabel=""):
    plt.title(title, loc="left", fontweight="bold", pad=18)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.15)
    plt.tight_layout()
    plt.savefig(charts / name, dpi=160)
    plt.close()

a1 = pd.read_csv(results / "a1_yearly_totals.csv")
plt.figure(figsize=(9, 5))
plt.bar(a1.YEAR.astype(str), a1.SPENDING_BN)
finish("01_total_spending.png", "Medicare Part D gross drug spending, 2020–2024", ylabel="$ billions")

a2 = pd.read_csv(results / "a2_top_drugs_2024.csv").head(10).iloc[::-1]
plt.figure(figsize=(9, 6))
plt.barh(a2.BRAND_NAME, a2.SPENDING_BN)
finish("02_top10_drugs_2024.png", "Highest-spending drugs in 2024", xlabel="$ billions")

a3 = pd.read_csv(results / "a3_class_trend.csv")
plt.figure(figsize=(9, 5.5))
for drug_class, frame in a3.groupby("DRUG_CLASS"):
    plt.plot(frame.YEAR, frame.SPENDING_BN, marker="o", label=drug_class)
plt.legend()
finish("03_drug_class_trends.png", "Spending by selected drug classes", ylabel="$ billions")

a4 = pd.read_csv(results / "a4_price_volume.csv")
plt.figure(figsize=(10, 5))
plt.bar(a4.COMPONENT, a4.CHANGE_BN)
plt.xticks(rotation=12, ha="right")
finish("04_growth_decomposition.png", "Expenditure growth components", ylabel="$ billions")

a6 = pd.read_csv(results / "a6_brand_vs_generic_2024.csv").set_index("BRAND_OR_GENERIC")
plt.figure(figsize=(8, 4))
plt.barh(["Claims share", "Spending share"], [a6.loc["Generic", "CLAIMS_SHARE_PCT"], a6.loc["Generic", "SPEND_SHARE_PCT"]], label="Generic (proxy)")
plt.barh(["Claims share", "Spending share"], [a6.loc["Brand", "CLAIMS_SHARE_PCT"], a6.loc["Brand", "SPEND_SHARE_PCT"]], left=[a6.loc["Generic", "CLAIMS_SHARE_PCT"], a6.loc["Generic", "SPEND_SHARE_PCT"]], label="Brand (proxy)")
plt.legend()
finish("05_brand_vs_generic.png", "2024 share of claims and spending", xlabel="Percent")

concentration = results / "a5_concentration_2024.csv"
if concentration.exists():
    a5 = pd.read_csv(concentration)
    plt.figure(figsize=(9, 5))
    plt.plot(a5.RNK / a5.N * 100, a5.CUM_SPEND_SHARE * 100)
    plt.plot([0,100],[0,100],"--",alpha=0.5)
    finish("06_concentration.png", "2024 cumulative spending concentration", xlabel="Share of drugs (%)", ylabel="Share of spending (%)")
else:
    print("Skipped concentration PNG (results/a5_concentration_2024.csv not yet uploaded).")

print("Saved PNG charts in", charts)
