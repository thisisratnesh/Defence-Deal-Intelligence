# This class saves structured deals into CSV file with deduplication

import csv
import os
from services.storage_base import StorageWriter


class CSVStorageWriter(StorageWriter):
    """
    CSV-based storage implementation.
    """

    def __init__(self, file_path: str):
        """
        Initialize CSV file path.

        :param file_path: Path where CSV will be stored
        """
        self.file_path = file_path

        # Fixed schema for CSV
        self.fieldnames = [
            "buyer",
            "seller",
            "product",
            "quantity",
            "deal_value",
            "currency",
            "deal_date",
            "source_url"
        ]

    def _get_existing_urls(self):
        """
        Load already saved source URLs to prevent duplicates.

        :return: Set of existing URLs
        """

        existing_urls = set()

        # If CSV doesn't exist yet, nothing to load
        if not os.path.exists(self.file_path):
            return existing_urls

        try:
            with open(self.file_path, mode="r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    existing_urls.add(row.get("source_url"))

        except Exception as error:
            print(f"Failed to read CSV file: {error}")

        return existing_urls

    def save_structured_deals(self, structured_deals: list):
        """
        Append structured deals into CSV file safely.

        :param structured_deals: List of structured deal dictionaries
        """

        existing_urls = self._get_existing_urls()

        file_exists = os.path.exists(self.file_path)

        try:
            with open(self.file_path, mode="a", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

                # Write header only when creating new file
                if not file_exists:
                    writer.writeheader()

                for deal in structured_deals:
                    source_url = deal.get("source_url")

                    # Skip duplicate entries
                    if source_url in existing_urls:
                        continue

                    writer.writerow({
                        "buyer": deal.get("buyer"),
                        "seller": deal.get("seller"),
                        "product": deal.get("product"),
                        "quantity": deal.get("quantity"),
                        "deal_value": deal.get("deal_value"),
                        "currency": deal.get("currency"),
                        "deal_date": deal.get("deal_date"),
                        "source_url": source_url
                    })

        except Exception as error:
            print(f"Failed writing CSV: {error}")
