import os
import timeit
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
llm = ChatOpenAI(openai_api_key=os.getenv(
    "OPENAI_API_KEY"), model_name='gpt-3.5-turbo')


def timeit_wrapper(func):
    '''Decorator for timing the function'''

    def wrap(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()

        print(func.__name__, " - ",  kwargs.get('type'),
              'Response Time : ', round((end-start), 2))
        return result
    return wrap


@timeit_wrapper
def get_ai_response(prompt: str, type: str = ''):
    return llm.predict(prompt)


def get_query(requirement: str, db_type: str, table_name: str, schema: str):
    prompt = PromptTemplate.from_template(
        """Generate an sql query to fetch {requirement} from a {db_type} table {table_name} with schema {schema}
        
        You may add additional columns in the query that can better explain the user's need.
        Do not explain the query and the only output should be the query and nothing else.""")
    required_prompt = prompt.format(requirement=requirement,
                                    schema=schema, table_name=table_name, db_type=db_type)

    res = get_ai_response(prompt=required_prompt, type='query_generation')
    return res.strip()


def get_mongo_query(requirement: str, db_schema):
    prompt = PromptTemplate.from_template(
        """Generate a mongo query for to fetch {requirement} from a mongo database with schema {db_schema}
        
        You may add additional columns in the query that can better explain the user's need.
        Do not explain the query and the only output should be the query and nothing else. Ensure that the parameters are enclosed in single quotes""")
    required_prompt = prompt.format(
        requirement=requirement, db_schema=db_schema)

    res = get_ai_response(prompt=required_prompt, type='query_generation')
    return res.strip()


def get_query_database(requirement: str, db_type: str, tables: list[str], schema: str):
    prompt = PromptTemplate.from_template(
        """Generate an sql query to fetch {requirement} from a {db_type} database with tables {tables} and with schema {schema}
        
        You may add additional columns in the query that can better explain the user's need.
        Do not explain the query and the only output should be the query and nothing else.""")
    required_prompt = prompt.format(requirement=requirement,
                                    schema=schema, tables=tables, db_type=db_type)

    res = get_ai_response(prompt=required_prompt, type='query_generation')
    return res.strip()


def get_parsed_result(requirement: str, result: str):
    prompt = PromptTemplate.from_template(
        """You are an sql result interpretation agent which explains the result of an sql query with respect to a particular requirement. Your explanation must be valid and must be able to explain the result of the sql query with respect to the requirement. Ensure that the interpretation encompasses the entire result as the user does not have accesss to the result data and can only see the interpretation. Do not reply with anything other than the valid explanation. Do not reply with any other wording or text other than just the explanation.
        
        The requirement is {requirement}

        The result is {result}
        """)

    required_prompt = prompt.format(requirement=requirement, result=result)
    res = get_ai_response(prompt=required_prompt, type='result_interpretation')
    return res.strip()


def get_visualization_suggestion(requirement: str, query: str):
    prompt = PromptTemplate.from_template(
        """Suggest a graph names that can best help interpret the following {requirement} and the {query}.
        
        --- Example ---
        Requirement : What is the average salary of employees in each department?
        Query : SELECT AVG(salary) FROM employee GROUP BY department;

        --- Output ---
        Bargraph, Histogram

        The output should strictly be of the above format and nothing else.


        """)

    required_prompt = prompt.format(requirement=requirement, query=query)

    res = get_ai_response(prompt=required_prompt,
                          type='visualization_suggestion')
    return res.strip()


def get_python_script(vis_desc: str, vis_suffix: str, vis_requirement: str, chart_type: str):
    prompt = f"""

    Generate a {chart_type} for the purpose of {vis_requirement}

    {vis_desc}

    -------

    {vis_suffix}


    Do not render this graph on screen and instead save this figure to a file called temp_files/image.jpg
    Do not add any extra text or comments in the code and return only the python code without any additional marksups or text.


    """

    res = get_ai_response(prompt=prompt, type='python_script')
    return res.strip()
