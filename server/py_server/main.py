import json
import sys
import repository as rep
import llmservice as gen
import logging
from fastapi import FastAPI

app = FastAPI()


# Logging config
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
debug_handler = logging.FileHandler('debug_log.log', mode='a')
debug_handler.setLevel(logging.DEBUG)
info_handler = logging.FileHandler('info_log.log', mode='a')
info_handler.setLevel(logging.INFO)
warn_handler = logging.FileHandler('warn_log.log', mode='a')
warn_handler.setLevel(logging.WARNING)

handlers = [debug_handler, info_handler, warn_handler]
for handler in handlers:
    logging.getLogger('').addHandler(handler)
# End of logging config


def query_pipeline(user_input: str = ''):

    # Fetch db schema from database
    data = {
        'table_name': 'student',
        'db_type': 'postgres',
        'requirement': user_input
    }

    data['db_schema'] = rep.get_table_schema(table_name=data['table_name'])

    data['query'] = gen.get_query(
        requirement=user_input, db_type='postgres', table_name=data['table_name'], schema=data['db_schema'])

    try:
        query_result = rep.get_query_result(
            table_name=data['table_name'], query=data['query'])
        data['result'] = query_result.get(
            'results', [])
        data['col_names'] = query_result.get('col_names', [])
    except:
        logging.warning('Error in pipeline', file=sys.stderr)

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
    logging.info(json.dumps(data, indent=2))
    data['visualization_recommendation'] = visualization_pipeline(data)
    if additional_info:
        return data
    else:
        return data.get('result', 'No such record found in the database')


@app.get("/visualization")
async def visualization(visualization_type: str, visualization_requirement: str):
    # return visualization_pipeline(data_dict)

    return {'visualization': 'bar chart'}
