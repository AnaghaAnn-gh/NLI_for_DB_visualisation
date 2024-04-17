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


def retrieve_schema(database_name):
    db = CLIENT[database_name]
    collection_names = db.list_collection_names()
    print('Collection Names:', collection_names)
    all_schemas = {}
    for collection_name in collection_names:
        collection = db[collection_name]
        documents = collection.find({})
        schema = {}
        for doc in documents:
            for key in doc:
                if key not in schema:
                    schema[key] = type(doc[key]).__name__
        all_schemas[collection_name] = schema
    return all_schemas


def perform_insert(insert_data, collection_name):
    # Access the database using the global CLIENT instance and DATABASE_NAME
    db = CLIENT[DATABASE_NAME]
    collection = db[collection_name]
    result = collection.insert_one(insert_data)
    return f"Insertion successful. Document ID: {result.inserted_id}"


def perform_extraction(query, collection_name):
    global extracted_data
    # Access the database using the global CLIENT instance and the specified DATABASE_NAME
    print("Query : ", query)
    db = CLIENT[DATABASE_NAME]
    collection = db[collection_name]
    documents = collection.find(query)
    extracted_data = list(documents)
    return extracted_data


llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

tool_insert = StructuredTool.from_function(
    perform_insert, description="Inserts data into the specified collection")
tool_extract = StructuredTool.from_function(
    perform_extraction, description="Extracts data from the specified collection")

agent_executor = initialize_agent(
    [tool_insert, tool_extract],
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


def run_query_with_user_input(user_query: str):
    global extracted_data
    extracted_data = None
    print(f"Retrieving {DATABASE_NAME} database schema...")
    schema = retrieve_schema(DATABASE_NAME)
    print("Database Schema:", schema)
    query_result = agent_executor.run(user_query)
    print(f"AI Agent: {query_result}")
    return [query_result, extracted_data]


def get_data_from_collection(collection_name: str):
    db = CLIENT[DATABASE_NAME]
    collection = db[collection_name]
    documents = collection.find({})
    data = list(documents)
    return data


def get_all_collection_names():
    db = CLIENT[DATABASE_NAME]
    collection_names = db.list_collection_names()
    return collection_names
