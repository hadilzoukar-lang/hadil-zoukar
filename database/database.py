import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="home.db"):
        self.db_path = db_path
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    def add_measurement(self, temperature, humidity):
        connection = self.connect()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection.execute(
            """
            INSERT INTO measurements
            (timestamp, temperature, humidity)
            VALUES (?, ?, ?)
            """,
            (timestamp, temperature, humidity)
        )

        connection.commit()
        connection.close()

    def add_event(self, event):
        connection = self.connect()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection.execute(
            """
            INSERT INTO events
            (timestamp, event)
            VALUES (?, ?)
            """,
            (timestamp, event)
        )

        connection.commit()
        connection.close()

    def get_measurements(self, limit=20):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT timestamp, temperature, humidity
            FROM measurements
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()

        connection.close()

        return results

    def get_events(self, limit=20):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT timestamp, event
            FROM events
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()

        connection.close()

        return results
