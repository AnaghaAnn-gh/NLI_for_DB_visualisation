import os
from dotenv import load_dotenv
import psycopg2
import logging
import pandas as pd

load_dotenv()


def get_connection():

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        return [cur, conn]
    except Exception as error:
        logging.error(error)


def drop_connection(cur, conn):
    cur.close()
    conn.close()


def get_table_schema(table_name: str) -> str:
    try:
        cur, conn = get_connection()
        query = f"select column_name, data_type from INFORMATION_SCHEMA.COLUMNS where table_name ='{table_name}';"
        cur.execute(query)
        results = cur.fetchall()

        drop_connection(cur, conn)

        schema = ''
        for result in results:
            schema += str(result[0]) + ':' + str(result[1]) + " "
        return schema.strip()
    except Exception as error:
        logging.error(error)


def get_database_schema(db_name: str) -> str:
    try:
        cur, conn = get_connection()
        query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        cur.execute(query)
        results = cur.fetchall()

        drop_connection(cur, conn)

        schema = ""
        tables = []
        for row in results:
            tables.append(row[0])
            schema += "Table Name : " + \
                str(row[0]) + " - " + get_table_schema(row[0]) + "\n"
        return {'tables': tables, 'schema': schema.strip()}
    except Exception as error:
        logging.error(error)


def get_query_result(table_name: str, query: str):
    try:
        cur, conn = get_connection()
        cur.execute(query)
        results = cur.fetchall()
        col_names = list(map(lambda x: x[0], cur.description))
        drop_connection(cur, conn)
        return {'results': results, 'col_names': col_names}
    except Exception as error:
        logging.error(error)


def insert_into_table(table_name: str, values: list[any]):
    try:
        cur, conn = get_connection()
        # cur.execute(query)
        # Add template for processing query
        conn.commit()
        drop_connection(cur, conn)
    except Exception as error:
        logging.error(error)
