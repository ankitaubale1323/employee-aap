import mysql.connector
import os

def get_db_connection():
    """
    Creates and returns a MySQL database connection.
    Works for:
    - Local XAMPP
    - AWS RDS (later)
    """

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),   # XAMPP default = empty
            database=os.getenv("DB_NAME", "employee_db"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return connection

    except mysql.connector.Error as err:
        print("❌ Database connection failed")
        print(err)
        raise
