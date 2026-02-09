import requests
import time


class NewsFetcher:
    """
    Fetches news articles from GDELT with retry and response validation.
    """

    def __init__(self, base_url: str, max_retries: int = 3, wait_seconds: int = 5):
        """
        Initialize fetcher configuration.

        :param base_url: GDELT API base URL
        :param max_retries: Retry attempts on failure
        :param wait_seconds: Delay between retries
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.wait_seconds = wait_seconds

    def fetch_articles(self, query: str, max_records: int = 50):
        """
        Fetch articles safely from GDELT.

        :param query: Search keywords
        :param max_records: Number of records requested
        :return: List of article dictionaries
        """

        request_parameters = {
            "query": query,
            "mode": "artlist",
            "format": "json",
            "maxrecords": max_records,
            "trans": "fulltext"
        }

        attempt_count = 0

        while attempt_count < self.max_retries:
            try:
                response = requests.get(self.base_url, params=request_parameters, timeout=10)
                print("RAW GDELT RESPONSE:")
                print(response.text[:1000])

                # Handle rate limiting
                if response.status_code == 429:
                    print("Rate limit hit. Waiting...")
                    time.sleep(self.wait_seconds)
                    attempt_count += 1
                    continue

                # If not successful status code
                if response.status_code != 200:
                    print(f"GDELT returned status {response.status_code}")
                    time.sleep(self.wait_seconds)
                    attempt_count += 1
                    continue

                # Try parsing JSON safely
                try:
                    response_data = response.json()
                except ValueError:
                    print("GDELT returned non-JSON response. Retrying...")
                    time.sleep(self.wait_seconds)
                    attempt_count += 1
                    continue

                # Extract articles cleanly
                articles_list = response_data.get("articles", [])

                return articles_list

            except requests.exceptions.RequestException as error:
                print(f"Attempt {attempt_count + 1} failed: {error}")
                time.sleep(self.wait_seconds)
                attempt_count += 1

        print("Max retries exceeded. Returning empty list.")
        return []
