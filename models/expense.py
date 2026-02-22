# models/expense.py
import sqlite3
from db import get_connection

class Expense:
    @staticmethod
    def create(owner_id, category_id, amount, date, description=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses (owner_id, category_id, amount, date, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (owner_id, category_id, amount, date, description)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT e.id, o.name, c.name, e.amount, e.date, e.description
                FROM expenses e
                LEFT JOIN owners o ON e.owner_id = o.id
                LEFT JOIN categories c ON e.category_id = c.id
                ORDER BY e.date DESC
                """
            )
            return cursor.fetchall()

