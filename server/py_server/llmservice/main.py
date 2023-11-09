import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import openai

load_dotenv()


def get_query(requirement: str):
    prompt = PromptTemplate.from_template(
        "Generate an sql query to fetch {requirement} from a {db_type} table {table_name} with schema {schema}")
    required_prompt = prompt.format(requirement="Get names of Top 10 users with highest expense",
                                    schema="id: uuid, name: string, user_expense: int", table_name="users", db_type="mysql")

    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    res = llm.predict(required_prompt)
    return res
