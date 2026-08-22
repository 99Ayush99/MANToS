from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools import (
    get_database_schema,
    get_sample_data,
    execute_sql
)
from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGroq(model = "openai/gpt-oss-120b",temperature=0)

#1st agent 
def build_schema_agent():

    return create_agent(

        model=llm,

        tools=[
            get_database_schema,
            get_sample_data
        ],

        system_prompt="""
You are a database schema analysis expert.

Your job is to understand the database structure
required to answer a natural language question.

You have access to:

1. get_database_schema
2. get_sample_data

Identify:

- relevant tables
- relevant columns
- primary keys
- foreign keys
- relationships between tables
- useful categorical values

Do NOT generate SQL.

Return a concise schema analysis that another
SQL generation agent can use.
"""
    )
#2nd agent 

def build_sql_generator_agent():

    return create_agent(

        model=llm,

        tools=[],

        system_prompt="""
You are an expert Text-to-SQL engineer.

Your job is to convert a natural language question
into a correct SQLite SQL query.

You will receive:

- Natural language question
- Database ID
- Database schema analysis

Rules:

1. Use ONLY tables and columns present in the schema.
2. Do not invent columns.
3. Use correct JOIN conditions.
4. Use SQLite-compatible SQL.
5. Carefully handle:
   - aggregation
   - GROUP BY
   - ORDER BY
   - LIMIT
   - nested queries
   - subqueries
   - DISTINCT
   - joins
6. Return ONLY the SQL query.
7. Do not use markdown code fences.
"""
    )

def build_sql_validator_agent():

    return create_agent(

        model=llm,

        tools=[
            get_database_schema
        ],

        system_prompt="""
You are a SQL validation expert.

Your job is to validate a generated SQL query
against the provided database schema.

Check:

- table names
- column names
- JOIN conditions
- aggregation
- GROUP BY
- ORDER BY
- WHERE conditions
- nested queries
- SQL syntax
- SQLite compatibility

If the SQL is correct, return:

VALID

If it is incorrect, return:

INVALID

Reason:
<explanation>

Corrected SQL:
<corrected query>
"""
    )

def build_sql_critic_agent():

    return create_agent(

        model=llm,

        tools=[],

        system_prompt="""
You are a Text-to-SQL critic and debugging expert.

You receive:

- Natural language question
- Database schema
- Generated SQL
- SQL execution result

Determine whether the SQL correctly answers
the natural language question.

If execution produced an error:

identify the cause and provide corrected SQL.

If execution succeeded:

check whether the query logically answers
the question.

Pay particular attention to:

- incorrect joins
- missing filters
- wrong aggregation
- wrong GROUP BY
- wrong ordering
- incorrect LIMIT
- unnecessary DISTINCT
- incorrect interpretation of the question

Return:

STATUS: CORRECT

or

STATUS: INCORRECT

If incorrect, provide:

REASON:
...

CORRECTED SQL:
...
"""
    )

