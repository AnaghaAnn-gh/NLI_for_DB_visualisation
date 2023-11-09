import repository as rep
import llmservice as gen


def pipeline(user_input: str):

    # Fetch db schema from database

    # db_schema = rep.get_schema()
    db_query = gen.get_query(user_input)
    print(db_query)


pipeline("What were the top ten users who has the most sales")
