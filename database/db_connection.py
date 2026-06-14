import mysql.connector
from mysql.connector import Error

conn = None


def get_connection():
    global conn
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root", 
            database="library_db",  
        )
        print("החיבור למסד הנתונים הצליח!")
    except Error as e:
        print(f"שגיאה בהתחברות למסד הנתונים: {e}")
        conn = None


def create_tables():
    if conn is None or not conn.is_connected():
        print("אין חיבור פעיל למסד הנתונים. לא ניתן ליצור טבלאות.")
        return

    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL, 
            is_available BIT DEFAULT 1
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowers (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL
        )
        """)

        conn.commit()

if __name__ == "__main__":
    get_connection()
    create_tables()