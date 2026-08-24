from src.agents.schema import build_schema_agent
from src.agents.sql_generator import build_sql_generator_agent
from src.agents.sql_validator import build_sql_validator_agent
from src.agents.sql_critic import build_sql_critic_agent
from src.tools.execute_sql import execute_sql
from rich import print

def get_agent_output(result):

    return result["messages"][-1].content


def run_nlq_to_sql(
    question: str,
    db_id: str
):

    state = {}

    print("\n" + "=" * 60)
    print("STEP 1 — SCHEMA AGENT")
    print("=" * 60)

    schema_agent = build_schema_agent()

    schema_result = schema_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Database ID: {db_id}

Natural Language Question:
{question}

Analyze the database schema required to answer this question.
"""
            )
        ]
    })

    state["schema"] = get_agent_output(schema_result)
    state["schema agent result"] = schema_result
    print(state["schema"])


    print("\n" + "=" * 60)
    print("STEP 2 — SQL GENERATOR")
    print("=" * 60)

    sql_agent = build_sql_generator_agent()

    sql_result = sql_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Database ID:
{db_id}

Question:
{question}

Schema Analysis:
{state["schema"]}

Generate the SQL query.
"""
            )
        ]
    })

    state["sql"] = get_agent_output(sql_result)
    state["sql agent result"] = sql_result
    print("Generated SQL:")
    print(state["sql"])


    print("\n" + "=" * 60)
    print("STEP 3 — SQL VALIDATOR")
    print("=" * 60)

    validator_agent = build_sql_validator_agent()

    validation_result = validator_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Database ID:
{db_id}

Question:
{question}

Schema:
{state["schema"]}

Generated SQL:
{state["sql"]}

Validate this SQL.
"""
            )
        ]
    })

    state["validation"] = get_agent_output(validation_result)
    state["validation agent result"] = validation_result
    print(state["validation"])


    print("\n" + "=" * 60)
    print("STEP 4 — SQL EXECUTION")
    print("=" * 60)

    

    execution_result = execute_sql.invoke({
        "db_id": db_id,
        "sql": state["sql"]
    })

    state["execution"] = execution_result

    print(state["execution"])


    print("\n" + "=" * 60)
    print("STEP 5 — SQL CRITIC")
    print("=" * 60)

    critic_agent = build_sql_critic_agent()

    critic_result = critic_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Question:
{question}

Database:
{db_id}

Schema:
{state["schema"]}

Generated SQL:
{state["sql"]}

Validation:
{state["validation"]}

Execution Result:
{state["execution"]}

Critically evaluate the SQL.
"""
            )
        ]
    })

    state["critic"] = get_agent_output(critic_result)
    state["critic agent result"] = critic_result
    print(state["critic"])

    
    print("\n" + "=" * 60)
    print("FINAL STATE")
    print("=" * 60)
    print(state)
    

    return state