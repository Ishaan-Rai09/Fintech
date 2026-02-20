import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    cursor = conn.cursor()
    
    with open('schema.sql', 'r') as f:
        schema = f.read()
    
    # Split statements by semicolon and execute
    statements = schema.split(';')
    for statement in statements:
        if statement.strip():
            cursor.execute(statement)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
