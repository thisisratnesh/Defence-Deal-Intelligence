# This class saves structured deals into SQLite database
# SQLite is built-in in Python and requires no external server

import sqlite3
from services.storage_base import StorageWriter


class DatabaseStorageWriter(StorageWriter):
    """
    SQLite based storage implementation.
    """

    def __init__(self, database_path: str):
        """
        Initialize database and ensure table exists.

        :param database_path: SQLite database file path
        """
        self.database_path = database_path

        # Create table if it does not already exist
        self._initialize_database()

    def _initialize_database(self):
        """
        Create deals table for storing structured records.
        """

        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    buyer TEXT,
                    seller TEXT,
                    product TEXT,
                    quantity TEXT,
                    deal_value TEXT,
                    currency TEXT,
                    deal_date TEXT,
                    source_url TEXT UNIQUE
                )
            """)

            connection.commit()
            connection.close()

        except Exception as error:
            print(f"Database initialization failed: {error}")

    def save_structured_deals(self, structured_deals: list):
        """
        Insert structured deals into SQLite database.
        Duplicate entries are avoided using UNIQUE constraint on source_url.

        :param structured_deals: List of structured deal dictionaries
        """

        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()

            for deal in structured_deals:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO deals (
                            buyer,
                            seller,
                            product,
                            quantity,
                            deal_value,
                            currency,
                            deal_date,
                            source_url
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        deal.get("buyer"),
                        deal.get("seller"),
                        deal.get("product"),
                        deal.get("quantity"),
                        deal.get("deal_value"),
                        deal.get("currency"),
                        deal.get("deal_date"),
                        deal.get("source_url")
                    ))

                except Exception as insert_error:
                    print(f"Failed inserting deal: {insert_error}")

            connection.commit()
            connection.close()

        except Exception as error:
            print(f"Database write failed: {error}")
