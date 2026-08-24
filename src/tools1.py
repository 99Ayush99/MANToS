import sqlite3
import json
import os

from langchain.tools import tool


SPIDER_DB_PATH = "spider_data/database"


@tool
def get_database_schema(db_id: str) -> str:
    """
    Get the complete schema of a Spider database.
    
    Returns tables, columns, primary keys and foreign keys.
    """

    db_path = os.path.join(
        SPIDER_DB_PATH,
        db_id,
        f"{db_id}.sqlite"
    )

    if not os.path.exists(db_path):
        return f"Database not found: {db_id}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        """
    ).fetchall()

    schema = []

    for (table,) in tables:

        columns = cursor.execute(
            f'PRAGMA table_info("{table}")'
        ).fetchall()

        foreign_keys = cursor.execute(
            f'PRAGMA foreign_key_list("{table}")'
        ).fetchall()

        table_info = {
            "table": table,
            "columns": [
                {
                    "name": col[1],
                    "type": col[2],
                    "primary_key": bool(col[5])
                }
                for col in columns
            ],
            "foreign_keys": [
                {
                    "column": fk[3],
                    "references_table": fk[2],
                    "references_column": fk[4]
                }
                for fk in foreign_keys
            ]
        }

        schema.append(table_info)

    conn.close()

    return json.dumps(schema, indent=2)

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


