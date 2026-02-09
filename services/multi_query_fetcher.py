# This service runs multiple search queries against GNews
# and merges results into one deduplicated article list

class MultiQueryFetcher:
    """
    Fetches articles using multiple high-signal queries
    and removes duplicate URLs.
    """

    def __init__(self, news_fetcher):
        """
        :param news_fetcher: instance of GNewsFetcher
        """
        self.news_fetcher = news_fetcher

    def fetch_from_queries(self, queries, max_per_query=5):
        """
        Run multiple queries and merge unique articles.

        :param queries: list of query strings
        :param max_per_query: articles per query
        :return: list of unique articles
        """

        all_articles = []
        seen_urls = set()

        for query in queries:

            articles = self.news_fetcher.fetch_articles(
                query=query,
                max_records=max_per_query
            )

            for article in articles:
                url = article.get("url")

                # Skip if already collected
                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)
                all_articles.append(article)

        return all_articles
