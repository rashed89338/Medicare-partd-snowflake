"""Export MARTS.V_DRUG_YEAR from a local DuckDB reproduction as JSON {rows, meta}."""
import json, re, sys
from pathlib import Path
import duckdb

csv_path, proj = Path(sys.argv[1]), Path(sys.argv[2])
sql = proj / "sql"
con = duckdb.connect()
for s in ("RAW", "STAGING", "MARTS"):
    con.execute(f"CREATE SCHEMA {s}")
cols = (proj / "scripts" / "raw_columns.txt").read_text().split()
types = ", ".join(f"'{c}': 'VARCHAR'" for c in cols)
con.execute(f"CREATE TABLE RAW.SPENDING_BY_DRUG AS SELECT * FROM read_csv('{csv_path}', header=true, columns={{{types}}})")

def stmts(t):
    t = "\n".join(l for l in t.splitlines() if not l.strip().upper().startswith("USE "))
    return [s for s in t.split(";") if re.sub(r"--.*", "", s).strip()]

for f in ("03_staging.sql", "04_marts.sql"):
    for s in stmts((sql / f).read_text()):
        con.execute(s)

df = con.execute("""SELECT REPLACE(BRAND_NAME,'*','') AS BRAND_NAME,
  GENERIC_NAME, BRAND_OR_GENERIC, DRUG_CLASS, YEAR,
  ROUND(TOTAL_SPENDING, 0) AS TOTAL_SPENDING,
  ROUND(DOSAGE_UNITS, 0) AS DOSAGE_UNITS, CLAIMS
  FROM MARTS.V_DRUG_YEAR ORDER BY YEAR, TOTAL_SPENDING DESC""").df()
rows = json.loads(df.to_json(orient="records"))
meta = [
    {"label": "Source", "value": "CMS Medicare Part D Spending by Drug, 2020-2024, 14,536 rows"},
    {"label": "03_staging.sql", "value": (sql / "03_staging.sql").read_text(), "type": "code", "lang": "sql"},
    {"label": "04_marts.sql", "value": (sql / "04_marts.sql").read_text(), "type": "code", "lang": "sql"},
    {"label": "export_dashboard_data.py", "value": Path(__file__).read_text(), "type": "code", "lang": "python"}
]
(proj / "results" / "drug_year.json").write_text(json.dumps({"rows": rows, "meta": meta}, separators=(",", ":")))
print(len(rows), df.TOTAL_SPENDING.sum() / 1e9)
