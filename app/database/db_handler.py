# app/database/db_handler.py
import mysql.connector
from mysql.connector import Error


class DBHandler:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='library_management'
            )
            print("Database connection established")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def execute_query(self, query, params=None, fetch=False):
        """Execute a SQL query"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetch:
                return cursor.fetchall()
            else:
                self.connection.commit()
                if cursor.rowcount > 0:
                    return True
                return False

        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")


# Singleton instance
db = DBHandler()

