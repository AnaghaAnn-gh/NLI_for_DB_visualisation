import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate.from_template(
    "Generate an sql query to fetch {requirement} from a table {table_name} with schema {schema}")
required_prompt = prompt.format(requirement="Get names of Top 10 users with highest expense",
                                schema="id: uuid, name: string, user_expense: int", table_name="users")

llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
res = llm.predict(required_prompt)
print(res)
