# db.py
import sqlite3
from config import DB_PATH

def get_connection():
    """Devuelve una conexión al SQLite DB."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Crea las tablas si no existen."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Propietarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )
        """)
        # Rubros (categorías)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        # Ingresos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
                category_id INTEGER,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY(owner_id) REFERENCES owners(id),
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)
        # Egresos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
                category_id INTEGER,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY(owner_id) REFERENCES owners(id),
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada.")

