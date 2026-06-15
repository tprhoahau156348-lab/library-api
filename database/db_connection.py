import mysql.connector
from mysql.connector import Error

conn = None

def get_connection():
    global conn

    try:
        if conn is None or not conn.is_connected():
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="root",
                database="library_db"
            )

        return conn

    except Error:
        return None


def create_tables():
    if conn is None or not conn.is_connected():
        return

    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            borrows_total INT NOT NULL DEFAULT 0
        )
        """)


        cursor.execute ("""
        CREATE TABLE IF NOT EXISTS books (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            genre ENUM(
                'Fiction',
                'Non-Fiction',
                'Science',
                'History',
                'Other'
            ),
            is_available BOOLEAN NOT NULL DEFAULT TRUE,
            borrowed_by_member_id INT NULL,
            
            FOREIGN KEY (borrowed_by_member_id) REFERENCES members(id) ON DELETE SET NULL
        )
        """)



        conn.commit()