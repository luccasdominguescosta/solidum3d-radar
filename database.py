from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd


DB_PATH = Path("solidum_radar.db")


def save_snapshot(df: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        df.to_sql("opportunities", conn, if_exists="append", index=False)


def read_all(db_path: Path = DB_PATH) -> pd.DataFrame:
    if not db_path.exists():
        return pd.DataFrame()
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query("SELECT * FROM opportunities", conn)
