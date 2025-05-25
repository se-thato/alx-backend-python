import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connects to the MySQL server (without specifying a DB)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='theplanetisflat'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='theplanetisflat',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it does not exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
    );
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Inserts data from CSV into the user_data table if not already present."""
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check for duplicates based on email
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (row['email'],))
                if cursor.fetchone():
                    continue 

                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
