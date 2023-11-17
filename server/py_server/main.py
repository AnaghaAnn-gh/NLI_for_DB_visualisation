import sys
import repository as rep
import llmservice as gen


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
        data['result'] = rep.get_query_result(
            table_name=data['table_name'], query=data['query'])
    except:
        print('Error in pipeline', file=sys.stderr)
        print(data)

    return data


def visualization_pipeline(data_dict: dict[str, str]):
    data_dict['visualization'] = gen.get_visualization_suggestion(
        requirement=data_dict['requirement'], query=data_dict['query'])

    print(data_dict['visualization'])
    return data_dict


data = query_pipeline('Who is the best worst and how can I contact him/her?')
print(data)
visualization_pipeline(data_dict=data)
