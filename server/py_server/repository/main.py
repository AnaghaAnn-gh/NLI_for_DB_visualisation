import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    return [cur, conn]


def drop_connection(cur, conn):
    cur.close()
    conn.close()


def get_table_schema(table_name: str) -> str:
    cur, conn = get_connection()
    query = f"select column_name, data_type from INFORMATION_SCHEMA.COLUMNS where table_name ='{table_name}';"
    cur.execute(query)
    results = cur.fetchall()
    print(results)
    drop_connection(cur, conn)

    schema = ''
    for result in results:
        schema += str(result[0]) + ':' + str(result[1]) + " "
    return schema.strip()


def get_query_result(table_name: str, query: str):
    cur, conn = get_connection()
    cur.execute(query)
    results = cur.fetchall()
    drop_connection(cur, conn)
    return results


def insert_into_table(table_name: str, values: list[any]):
    cur, conn = get_connection()
    # cur.execute(query)
    # Add template for processing query
    conn.commit()
    drop_connection(cur, conn)
