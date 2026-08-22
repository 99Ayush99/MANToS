from src.pipeline import run_nlq_to_sql


question = """
How many singers do we have?
"""

db_id = "concert_singer"

result = run_nlq_to_sql(
    question=question,
    db_id=db_id
)

print("\n\nFINAL SQL")
print(result["sql"])