from db_connection import get_connection


class MembreDb:
      

    def create_members(self, name, email):
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute("""
            INSERT INTO members (name, email)
            VALUES (%s, %s)
            """, (name, email))
                
            conn.commit()

    
    def get_all_member(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM members")
            rows = cursor.fetchall()
            return rows
        
    def get_member_by_id(self, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM members
            WHERE id = %s
            """, (member_id,))
            return cursor.fetchone()
        
    def update_member(self,name, email, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE members
            SET name = %s,
                email = %s
            WHERE id = %s
            """, (name, email, member_id)) 

            conn.commit()

    def delete_member(self, member_id):
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute("""
            DELETE FROM members
            WHERE id = %s
            """, (member_id,))
                
            conn.commit()

    def deactivate_member(self, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE members SET is_active = FALSE WHERE id = %s
            """, (member_id,))
            conn.commit()

    def activate_member(self, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE members SET is_active = TRUE WHERE id = %s
            """, (member_id,))
            conn.commit()

    def increment_borrows(self, member_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE members SET borrows_total = borrows_total + 1 WHERE id = %s
            """, (member_id,))
            conn.commit()

    def count_active_members(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = TRUE")
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_top_member(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT id, borrows_total FROM members 
            ORDER BY borrows_total DESC 
            LIMIT 1
            """)
            return cursor.fetchone()