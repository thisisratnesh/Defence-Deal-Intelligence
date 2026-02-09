# This service fetches full article content from GNews API

import requests


class GNewsFetcher:
    """
    Fetches news articles with full content using GNews API.
    """

    def __init__(self, api_key: str, language: str = "en"):
        """
        Initialize GNews API client.

        :param api_key: GNews API token
        :param language: language filter (default English)
        """
        self.api_key = api_key
        self.language = language
        self.base_url = "https://gnews.io/api/v4/search"

    def fetch_articles(self, query: str, max_records: int = 10):
        """
        Fetch articles related to query.

        :param query: search keywords
        :param max_records: number of articles to fetch
        :return: list of article dictionaries
        """

        try:
            params = {
                "q": query,
                "lang": self.language,
                "max": max_records,
                "token": self.api_key
            }

            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            # GNews returns articles inside "articles" key
            return data.get("articles", [])

        except Exception as error:
            print(f"GNews fetch failed: {error}")
            return []
