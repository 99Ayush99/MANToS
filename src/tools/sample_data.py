import sqlite3
import json
import os

from langchain.tools import tool


SPIDER_DB_PATH = "spider_data/database"

@tool
def get_sample_data(db_id: str, table_name: str) -> str:
    """
    Return a small sample of rows from a table.
    Useful for understanding actual data values.
    """

    db_path = os.path.join(
        SPIDER_DB_PATH,
        db_id,
        f"{db_id}.sqlite"
    )

    if not os.path.exists(db_path):
        return f"Database not found: {db_id}"

    try:

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        cursor.execute(
            f'SELECT * FROM "{table_name}" LIMIT 5'
        )

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        conn.close()

        return json.dumps({
            "columns": columns,
            "rows": rows
        }, default=str)

    except Exception as e:
        return f"Error: {str(e)}"
