from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.database_schema import get_database_schema
from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGroq(model = "openai/gpt-oss-120b",temperature=0)

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