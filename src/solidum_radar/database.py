from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("solidum_radar.db")
TABLE_NAME = "opportunities"


def save_snapshot(
    df: pd.DataFrame,
    db_path: Path = DB_PATH,
) -> None:

    with sqlite3.connect(db_path) as conn:

        if _table_exists(conn, TABLE_NAME):

            existing_columns = _get_table_columns(
                conn,
                TABLE_NAME,
            )

            new_columns = set(df.columns)

            if existing_columns != new_columns:

                df.to_sql(
                    TABLE_NAME,
                    conn,
                    if_exists="replace",
                    index=False,
                )

                return

        df.to_sql(
            TABLE_NAME,
            conn,
            if_exists="append",
            index=False,
        )


def read_all(
    db_path: Path = DB_PATH,
) -> pd.DataFrame:

    if not db_path.exists():
        return pd.DataFrame()

    with sqlite3.connect(db_path) as conn:

        if not _table_exists(
            conn,
            TABLE_NAME,
        ):
            return pd.DataFrame()

        return pd.read_sql_query(
            f"SELECT * FROM {TABLE_NAME}",
            conn,
        )


def _table_exists(
    conn: sqlite3.Connection,
    table_name: str,
) -> bool:

    cursor = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table_name,),
    )

    return cursor.fetchone() is not None


def _get_table_columns(
    conn: sqlite3.Connection,
    table_name: str,
) -> set[str]:

    cursor = conn.execute(
        f"PRAGMA table_info({table_name})"
    )

    return {
        row[1]
        for row in cursor.fetchall()
    }
