from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGroq(model = "openai/gpt-oss-120b",temperature=0)

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

identify the cause

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

REASON
...

##Output format:
{{
    "status": "<CORRECT or INCORRECT>",
    "reason": "<explanation>",
}}
...
"""
    )