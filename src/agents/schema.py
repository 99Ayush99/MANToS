from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.database_schema import get_database_schema
from src.tools.sample_data import get_sample_data

from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGroq(model = "openai/gpt-oss-120b",temperature=0)

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