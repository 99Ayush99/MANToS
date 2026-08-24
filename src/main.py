from src.pipeline import run_nlq_to_sql
from src.utils.json_extractor import extract_json_from_string

question = """
How many singers do we have?
"""

db_id = "concert_singer"

result = run_nlq_to_sql(
    question=question,
    db_id=db_id
)

result_json_critic = extract_json_from_string(result["critic"])

if result_json_critic["status"] == "CORRECT":

    print("\n\nFINAL SQL")
    print(result["sql"])
else:
    print("\n\nFinal SQL is incorrect. Please check the reason and corrected SQL below:")
    print(f"Reason: {result_json_critic['reason']}")