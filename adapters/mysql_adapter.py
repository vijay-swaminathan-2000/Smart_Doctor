import pymysql
from adapters.aws_adapter import get_secret
import json

def get_connection():
    print("Fetching database credentials...")
    database_credentials = json.loads(get_secret("database/prod"))

    print("Establishing connection to database...")
    connection = pymysql.connect(host=database_credentials["database_host"],
                                 user=database_credentials["database_username"],
                                 password=database_credentials["database_password"],
                                 database=database_credentials["database_db_name"])
    print("Connection to database established successfully.")
    return connection

def fetch_data(query):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    sql_results = cursor.fetchall()
    cursor.close()
    connection.close()
    return sql_results

def insert_data(query, data):
    connection = get_connection()
    cursor = connection.cursor()

    for key, value in data.items():
        cursor.execute(query, (key, value))

    connection.commit()
    cursor.close()
    connection.close()