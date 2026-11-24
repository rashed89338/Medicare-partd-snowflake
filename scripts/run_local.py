"""Run the Snowflake-style SQL pipeline locally with DuckDB for validation.
Usage: python scripts/run_local.py <path-to-cms-csv> <project-dir>
"""
import re
import sys
from pathlib import Path
import duckdb

csv_path, proj = Path(sys.argv[1]), Path(sys.argv[2])
sql_dir, out_dir = proj / "sql", proj / "results"
out_dir.mkdir(exist_ok=True)

con = duckdb.connect()
for s in ("RAW", "STAGING", "MARTS"):
    con.execute(f"CREATE SCHEMA {s}")

cols = (proj / "scripts" / "raw_columns.txt").read_text().split()
types = ", ".join(f"'{c}': 'VARCHAR'" for c in cols)
con.execute(f"CREATE TABLE RAW.SPENDING_BY_DRUG AS SELECT * FROM read_csv('{csv_path}', header=true, columns={{{types}}})")

def statements(text):
    text = "\n".join(l for l in text.splitlines() if not l.strip().upper().startswith("USE "))
    return [s.strip() for s in text.split(";") if re.sub(r"--.*", "", s).strip()]

for f in ("03_staging.sql", "04_marts.sql"):
    for stmt in statements((sql_dir / f).read_text()):
        res = con.execute(stmt)
        if stmt.lstrip().upper().startswith("SELECT") or "\nSELECT COUNT" in stmt:
            print(f, res.fetchall())

print("raw rows:", con.execute("SELECT COUNT(*) FROM RAW.SPENDING_BY_DRUG").fetchone())
print("dim_drug:", con.execute("SELECT COUNT(*) FROM MARTS.DIM_DRUG").fetchone())
print("fct_drug_year:", con.execute("SELECT COUNT(*) FROM MARTS.FCT_DRUG_YEAR").fetchone())

analysis = (sql_dir / "05_analysis.sql").read_text()
for block in analysis.split("-- @")[1:]:
    name, body = block.split("\n", 1)
    stmt = statements(body)[0]
    df = con.execute(stmt).df()
    df.to_csv(out_dir / f"{name.strip()}.csv", index=False)
    print(f"\n=== {name.strip()} ({len(df)} rows)")
    print(df.head(15).to_string(index=False))
