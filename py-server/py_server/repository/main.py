import mysql.connector

def connect_to_mysql(host, database, user, password):
    try:
        # Create a connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        if connection.is_connected():
            return connection
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Usage example
if __name__ == "__main__":
    db_host = "localhost"
    db_name = "your_database"
    db_user = "your_user"
    db_password = "your_password"

    db_connection = connect_to_mysql(db_host, db_name, db_user, db_password)

    if db_connection is not None:
        # You can perform database operations here
        # Don't forget to close the connection when done
        db_connection.close()
