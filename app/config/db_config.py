import mysql.connector
import os
import time

def get_db_connection():
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql"),
                user=os.getenv("DB_USER", "employee_user"),
                password=os.getenv("DB_PASSWORD", "root"),
                database=os.getenv("DB_NAME", "employee_db"),
                port=int(os.getenv("DB_PORT", 3306))
            )

            # Auto-create employees table if it doesn't exist
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    role VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

            return conn
        except Exception as e:
            print("Waiting for MySQL...", e)
            time.sleep(3)

    raise Exception("Could not connect to MySQL")
