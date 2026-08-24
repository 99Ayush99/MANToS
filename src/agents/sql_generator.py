from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGroq(model = "openai/gpt-oss-120b",temperature=0)

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