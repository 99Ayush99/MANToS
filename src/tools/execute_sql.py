import sqlite3
import json
import os

from langchain.tools import tool


SPIDER_DB_PATH = "spider_data/database"

@tool
def execute_sql(db_id: str, sql: str) -> str:
    """
    Execute a SQL query on a Spider SQLite database.

    Returns either the query results or an SQL error.
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

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ] if cursor.description else []

        conn.close()

        return json.dumps({
            "status": "success",
            "columns": columns,
            "rows": rows[:50],
            "row_count": len(rows)
        }, default=str)

    except Exception as e:

        return json.dumps({
            "status": "error",
            "error": str(e)
        })

