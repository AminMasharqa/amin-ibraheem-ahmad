import psycopg2
from psycopg2 import OperationalError

def check_table_exists(table_name):
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname="amin_db",
            user="amin",
            password="amin1234",
            host="localhost",
            port="5432"
        )
        
        cursor = connection.cursor()
        
        # Execute SQL query to check for the specified table
        cursor.execute(
            f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
        )
        exists = cursor.fetchone()[0]

        if exists:
            print(f"The '{table_name}' table exists in the database.")
        else:
            print(f"The '{table_name}' table does not exist in the database.")
    
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
    
    finally:
        # Close database connection
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    tables_to_check = ["genre", "artists", "songs", "ranking"]

    for table in tables_to_check:
        check_table_exists(table)
