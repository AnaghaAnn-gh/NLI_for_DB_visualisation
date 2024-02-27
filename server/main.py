import json
import os
import sys

import pandas as pd
import repository as rep
import llm as gen
import visualization as vis
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import mongo

app = FastAPI()


def query_pipeline(requirement: str = ''):

    # Fetch db schema from database
    data = {
        'table_name': 'student',
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

    print(json.dumps(data, indent=2))
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


@app.get("/mongo_query")
async def mongo_query(user_input: str, additional_info: bool = False):
    res = mongo.run_query_with_user_input(user_input)
    return {'data': res}


@app.get("/visualization")
async def visualization(user_input: str, chart_type: str, vis_requirement: str):
    # return visualization_pipeline(data_dict)
    data = query_pipeline(user_input)
    df = pd.DataFrame(data['result'], columns=data['col_names'])
    desc, suffix = vis.get_primer(
        df_dataset=df, df_name='df')
    print(desc)
    print(suffix)

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
