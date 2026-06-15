from db_connection import get_connection


class BookDB:

    def create_book(self, title, author, genre):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            INSERT INTO books(title, author, genre)
            VALUES (%s, %s, %s)
            """, (title, author, genre))
                
            conn.commit()

    def get_all_books(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return rows
        
    def get_book_by_id(self, book_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM books
            WHERE id = %s
            """, (book_id,))
            return cursor.fetchone()

    def update_book(self, title, author, genre, book_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE books
            SET title = %s,
                author = %s,  
                genre = %s
            WHERE id = %s
            """, (title, author, genre, book_id))
                
            conn.commit()
    
    def delete_book(self, book_id):
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute("""
            DELETE FROM books
            WHERE id = %s
            """, (book_id,))
                
            conn.commit()


    def set_available(self, book_id, val, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE books
            SET is_available = %s,
                borrowed_by_member_id = %s
            WHERE id = %s
            """, (val, member_id, book_id))
            conn.commit()

    def count_total_books(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books")
            result = cursor.fetchone()
            return result[0] if result else 0

    def count_available_books(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = TRUE")
            result = cursor.fetchone()
            return result[0] if result else 0

    def count_borrowed_books(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
            result = cursor.fetchone()
            return result[0] if result else 0

    def count_by_genre(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT genre, COUNT(*) as count 
            FROM books 
            GROUP BY genre
            """)
            return cursor.fetchall()

    def count_active_borrows_by_member(self, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT COUNT(*) FROM books 
            WHERE borrowed_by_member_id = %s
            """, (member_id,))
            result = cursor.fetchone()
            return result[0] if result else 0   