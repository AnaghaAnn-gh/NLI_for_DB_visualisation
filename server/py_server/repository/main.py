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


def get_table_schema(table_name: str):
    cur, conn = get_connection()
    query = f"select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name ='{table_name}';"
    cur.execute(query)
    results = cur.fetchall()
    # print(results)
    drop_connection(cur, conn)
    return results


def fetch_all_records():
    query = "select * from pages"
    cur, conn = get_connection()
    cur.execute(query)
    results = cur.fetchall()
    # print(results)
    drop_connection(cur, conn)
    return results
