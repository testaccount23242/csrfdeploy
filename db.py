# db.py
import psycopg2

DB_URL = "postgresql://csrf_db_user:DusFfExrvmbRfQxWBG7qUtwo30TczsSU@dpg-ctem62pu0jms739dbqi0-a.oregon-postgres.render.com/csrf_db"

# Connect to PostgreSQL database
with psycopg2.connect(DB_URL) as conn:
    with conn.cursor() as cursor:
        # Create the 'users' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            );
        ''')

        # Insert default admin and user accounts
        cursor.execute('''
            INSERT INTO users (username, password, role) VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        ''', ('admin', 'adminpass', 'admin'))

        cursor.execute('''
            INSERT INTO users (username, password, role) VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        ''', ('user1', 'userpass', 'user'))

        conn.commit()
        print("Database initialized with default users.")
