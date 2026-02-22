# models/income.py
import sqlite3
from db import get_connection

class Income:
    @staticmethod
    def create(owner_id, category_id, amount, date, description=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO incomes (owner_id, category_id, amount, date, description)
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
                SELECT i.id, o.name, c.name, i.amount, i.date, i.description
                FROM incomes i
                LEFT JOIN owners o ON i.owner_id = o.id
                LEFT JOIN categories c ON i.category_id = c.id
                ORDER BY i.date DESC
                """
            )
            return cursor.fetchall()

