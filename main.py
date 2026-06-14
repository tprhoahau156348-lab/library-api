import mysql.connector

def setup_database(): 
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS ;")
    print("[+] Database 'soldiers_db' is ready.")

    try:
        connection = mysql.connector.connect(
            hoshost="localhost",
            user="library_db",
            password="root"
            )
        cursor = connection.cursor()
