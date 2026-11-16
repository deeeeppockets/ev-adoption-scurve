"""Download the EV sales-share dataset used in this project.

Source: Our World in Data, "Share of new cars sold that are electric",
which republishes the IEA Global EV Outlook / Global EV Data Explorer.
"Electric" = battery-electric (BEV) + plug-in hybrid (PHEV) cars.

Usage (from the repo root):
    python src/fetch_data.py

Writes data/raw/electric-car-sales-share.csv. A frozen copy of this file is
committed to the repo so results are reproducible even if the source updates.
"""
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

URL = (
    "https://ourworldindata.org/grapher/electric-car-sales-share.csv"
    "?v=1&csvType=full&useColumnShortNames=true"
)
OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "electric-car-sales-share.csv"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    req = Request(URL, headers={"User-Agent": "ev-adoption-scurve (student project)"})
    with urlopen(req, timeout=60) as resp:
        OUT.write_bytes(resp.read())

    df = pd.read_csv(OUT)
    expected = {"entity", "code", "year", "ev_sales_share"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Unexpected schema, missing columns: {missing}")

    print(f"Saved {len(df)} rows to {OUT}")
    print(f"Years: {df.year.min()}-{df.year.max()} | entities: {df.entity.nunique()}")


if __name__ == "__main__":
    main()
