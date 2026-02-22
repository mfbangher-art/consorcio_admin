# models/owner.py
import sqlite3
from db import get_connection

class Owner:
    @staticmethod
    def create(name, phone=None, email=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO owners (name, phone, email) VALUES (?, ?, ?)",
                (name, phone, email)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, phone, email FROM owners")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(owner_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, phone, email FROM owners WHERE id = ?",
                (owner_id,)
            )
            return cursor.fetchone()

