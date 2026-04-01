# connect.py
import psycopg2
from config import load_config

def connect(config):
    """Connect to PostgreSQL database and return connection context"""
    try:
        with psycopg2.connect(**config) as conn:
            print("Connected to PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error:", error)

if __name__ == "__main__":
    config = load_config()
    connect(config)
