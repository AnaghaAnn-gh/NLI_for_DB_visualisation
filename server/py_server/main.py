import repository as rep
import llmservice as gen


def pipeline(user_input: str = ''):

    # Fetch db schema from database

    table_name = 'student'
    db_schema = rep.get_table_schema(table_name=table_name)
    print('Database schema : ', db_schema)
    db_query = gen.get_query(
        requirement=user_input, db_type='postgres', table_name=table_name, schema=db_schema)
    print('Generated Query : ', db_query)
    result = rep.get_query_result(table_name=table_name, query=db_query)
    print('Result : ', result)


# pipeline('Who is the top scoring student?')
