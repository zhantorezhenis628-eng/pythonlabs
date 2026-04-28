def create_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook(
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE,
                    first_name VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL UNIQUE
                )
            """)
            conn.commit()
            print("Table created")
    except Exception as e:
        conn.rollback()
        print(f"Error occured: {e}")

def create_table2(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE phones (
                    id         SERIAL PRIMARY KEY,
                    contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
                    phone      VARCHAR(20)  NOT NULL,
                    type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
                );
            """)
            conn.commit()
            print("Table created")
    except Exception as e:
        conn.rollback()
        print(f"Error occured: {e}")

def create_table2(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE groups (
                    id   SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            conn.commit()
            print("Table created")
    except Exception as e:
        conn.rollback()
        print(f"Error occured: {e}")