import os
import pickle

import pandas as pd
import repository as rep
import llm as gen
import visualization as vis
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import mongo

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def query_pipeline(requirement: str = ''):

    # Fetch db schema from database
    data = {
        'db_type': 'postgres',
        'requirement': requirement
    }

    # data['db_schema'] = rep.get_table_schema(table_name=data['table_name'])
    obj = rep.get_database_schema()
    data['db_schema'] = obj.get('schema')
    tables = obj.get('tables')
    # data['query'] = gen.get_query(
    #     requirement=user_input, db_type='postgres', table_name=data['table_name'], schema=data['db_schema'])

    print(data['db_schema'], tables)
    data['query'] = gen.get_query_database(
        requirement=requirement, db_type='postgres', schema=data['db_schema'], tables=tables)
    try:
        query_result = rep.execute_select_query(query=data['query'])
        results = query_result.get('results', [])
        data['result'] = results

        parsed_result = ''
        if len(results) > 0 and len(results) <= 10:
            parsed_result = gen.get_parsed_result(requirement, results)
        else:
            parsed_result = 'Too many records to parse. Will end up exhausting the API quota.'

        data['parsed_result'] = parsed_result
        data['col_names'] = query_result.get('col_names', [])
    except Exception as error:
        print(error)
        data['result'] = []
        print('Error in pipeline')

    # print(json.dumps(data, indent=2))
    return data


def visualization_pipeline(data_dict: dict[str, str]):
    visualization_recommendation = gen.get_visualization_suggestion(
        requirement=data_dict['requirement'], query=data_dict['query'])

    return visualization_recommendation


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/connect")


@app.get("/schema")
async def schema(table_name: str):
    return rep.get_table_schema(table_name)


@app.get("/query")
async def query(user_input: str, additional_info: bool = False):
    data = query_pipeline(user_input)
    # data['visualization_recommendation'] = visualization_pipeline(data)
    if additional_info:
        return data
    else:
        return data.get('result', 'No such record found in the database')


def isValid(res: str):
    checks = ['The provided JSON blob does not conform to the specified format',
              "I'm sorry", 'The provided JSON blob does not follow the specified format']

    for check in checks:
        if check in res:
            return False

    return True


@app.get("/mongo_query_2")
async def mongo_query(user_input: str, additional_info: bool = False):
    user_input += 'In the database by choosing the appropriate collection from the list of available collections'
    res, extracted_data = mongo.run_query_with_user_input(user_input)
    count = 0
    if not isValid(res) and count < 5:
        count += 1
        print('Try Number : ', count)
        res, extracted_data = mongo.run_query_with_user_input(user_input)

    if extracted_data is not None:
        for i in range(len(extracted_data)):
            extracted_data[i]['_id'] = str(extracted_data[i]['_id'])

    print('Extracted Data : ', extracted_data)
    return {'data': res, 'documents': extracted_data}


@app.get("/mongo_visualization")
async def mongo_visualization(user_input: str, chart_type: str, vis_requirement: str):
    data = mongo.get_data_from_collection(user_input)

    df = pd.DataFrame(data)
    os.makedirs('temp_files', exist_ok=True)
    df.to_csv('temp_files/data.csv', index=False)

    desc, suffix = vis.get_primer(
        df_dataset=df, df_name='df')
    print('Description : ', desc)
    print('Suffix : ', suffix)

    res = gen.get_python_script(vis_desc=desc,
                                vis_suffix=suffix, vis_requirement=vis_requirement, chart_type=chart_type)
    print(res)
    try:
        with open('temp_files/temp.py', 'w') as f:
            f.write(res)
        os.system('python temp_files/temp.py')

        image_path = Path('temp_files/image.jpg')
        if not image_path.is_file():
            return HTTPException(500, detail="Internal Server Error")
        return FileResponse(image_path, media_type="image/jpg")
    except:
        print('Error in generating graph')


@app.get("/visualization")
async def visualization(user_input: str, chart_type: str, vis_requirement: str):
    data = query_pipeline(user_input)
    df = pd.DataFrame(data['result'], columns=data['col_names'])
    os.makedirs('temp_files', exist_ok=True)
    df.to_csv('temp_files/data.csv', index=False)

    desc, suffix = vis.get_primer(
        df_dataset=df, df_name='df')
    print('Description : ', desc)
    print('Suffix : ', suffix)

    res = gen.get_python_script(vis_desc=desc,
                                vis_suffix=suffix, vis_requirement=vis_requirement, chart_type=chart_type)
    print(res)
    try:
        with open('temp_files/temp.py', 'w') as f:
            f.write(res)
        os.system('python temp_files/temp.py')

        image_path = Path('temp_files/image.jpg')
        if not image_path.is_file():
            return HTTPException(500, detail="Internal Server Error")
        return FileResponse(image_path, media_type="image/jpg")
    except:
        print('Error in generating graph')


@app.get("/db_schema")
async def db_schema():
    return {'data': rep.get_database_schema_json()}


@app.get('/mongo_schema')
async def mongo_collections():
    return {'data': mongo.retrieve_schema(os.getenv("DB_NAME"))}


@app.get('/mongo_collections')
async def mongo_schema():
    return {'data': mongo.get_all_collection_names()}


@app.get('/mongo_query')
async def mongo_query(user_input: str, additional_info: bool = False):
    db_schema = mongo.retrieve_schema(os.getenv("DB_NAME"))
    code = gen.get_mongo_query(user_input, db_schema)
    print(code)
    generator = f"""
import pickle
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool
import os
from pymongo import MongoClient

DB_USER = os.getenv("DB_USER")
DB_HOSTNAME = os.getenv("DB_MONGODB_HOSTNAME")
DB_SECRET = os.getenv("DB_PASSWORD")
DATABASE_NAME = os.getenv("DB_NAME")
print(DB_HOSTNAME, DB_USER, DB_SECRET, DATABASE_NAME)
CLIENT = MongoClient(DB_HOSTNAME, port=27017,
                    username=DB_USER, password=DB_SECRET)
extracted_data = None



db = CLIENT[DATABASE_NAME]

documents = {code}
data = list(documents)
for doc in data:
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])

with open("temp_files/output", "wb") as file:
    pickle.dump(data, file)
print("Results stored in output.txt")

    """

    l = []

    os.makedirs('temp_files', exist_ok=True)

    try:
        with open('temp_files/temp.py', 'w') as f:
            f.write(generator)

        os.system('python temp_files/temp.py')
        with open('temp_files/output', 'rb') as f:
            res = pickle.load(f)

        return {'data': "Here's the requested data", 'documents': res}
    except Exception as error:
        print(error)
        return {'data': 'Error in executing the query'}
