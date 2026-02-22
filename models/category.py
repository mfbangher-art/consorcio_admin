# models/category.py
import sqlite3
from db import get_connection

class Category:
    @staticmethod
    def create(name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (name,)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories")
            return cursor.fetchall()

