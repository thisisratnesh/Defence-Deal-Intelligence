# This class handles keyword-based filtering of articles


class KeywordEngine:
    """
    This class filters raw news articles using grouped keyword logic.
    It improves relevance and reduces noise.
    """

    def __init__(self, product_keywords: list, deal_keywords: list, context_keywords: list):
        """
        Initialize keyword groups.

        :param product_keywords: List of product/system related words (CUAS, drone, UAV, etc.)
        :param deal_keywords: List of deal related words (contract, order, awarded, etc.)
        :param context_keywords: List of defense/military context words
        """

        self.product_keywords = product_keywords
        self.deal_keywords = deal_keywords
        self.context_keywords = context_keywords

    def _text_contains_keyword(self, text: str, keyword_list: list):
        """
        Check if any keyword exists in given text.

        :param text: Combined article text
        :param keyword_list: Keywords to search for
        :return: True if any keyword found, else False
        """

        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()

        # Iterate through keywords
        for keyword in keyword_list:
            if keyword.lower() in text_lower:
                return True

        return False

    def filter_articles(self, articles: list):
        """
        Apply grouped keyword filtering logic.

        Article must match:
        - at least one product keyword
        - at least one deal keyword
        - at least one context keyword

        :param articles: Raw articles from GDELT
        :return: Filtered relevant articles
        """

        filtered_articles = []

        for article in articles:
            # Extract text fields safely
            title_text = article.get("title", "")
            description_text = article.get("seendescription", "")

            # Combine text for searching
            combined_text = f"{title_text} {description_text}"

            # Apply keyword group checks
            has_product = self._text_contains_keyword(combined_text, self.product_keywords)
            has_deal = self._text_contains_keyword(combined_text, self.deal_keywords)
            has_context = self._text_contains_keyword(combined_text, self.context_keywords)

            # If all three groups match, keep the article
            if has_product and has_deal and has_context:
                filtered_articles.append(article)

        return filtered_articles
