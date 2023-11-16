import os
import timeit
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import openai

load_dotenv()


def get_query(requirement: str, db_type: str, table_name: str, schema: str):
    prompt = PromptTemplate.from_template(
        "Generate an sql query to fetch {requirement} from a {db_type} table {table_name} with schema {schema}")
    required_prompt = prompt.format(requirement=requirement,
                                    schema=schema, table_name=table_name, db_type=db_type)

    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    start_time = timeit.default_timer()
    res = llm.predict(required_prompt)
    response_time = timeit.default_timer() - start_time
    print('Time to generate : ', response_time)
    return res.strip()
