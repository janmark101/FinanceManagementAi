import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Parametry połączenia
connection_params = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),        
}

try:
    # Nawiązanie połączenia
    conn = psycopg2.connect(**connection_params)

    # Tworzenie kursora do wykonywania zapytań
    cursor = conn.cursor()

    create_table = """
    CREATE TABLE IF NOT EXISTS expenses (
        id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        price FLOAT NOT NULL,
        company VARCHAR(255) ,
        category VARCHAR(255) 
    )
    """

    cursor.execute(create_table)
    conn.commit()

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
        print("Połączenie zamknięte.")
