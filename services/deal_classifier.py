# This class evaluates how likely an article represents a real deal or contract


class DealClassifier:
    """
    Classifies articles based on deal-related keyword scoring.
    """

    def __init__(self, score_threshold: int = 5):
        """
        Initialize classifier with minimum score required to mark article as deal.

        :param score_threshold: Minimum points to consider article a deal
        """
        self.score_threshold = score_threshold

        # Define scoring rules for deal signals
        self.scoring_rules = {
            "contract": 3,
            "deal": 3,
            "worth": 2,
            "million": 3,
            "billion": 3,
            "awarded": 2,
            "signed": 2,
            "order": 2,
            "$": 3
        }

    def classify_article(self, article: dict):
        """
        Calculate deal score for an article.

        :param article: Article dictionary from GDELT
        :return: Tuple (is_deal: bool, score: int)
        """

        # Extract article text safely
        title_text = article.get("title", "")
        description_text = article.get("seendescription", "")

        # Combine text for scoring
        combined_text = f"{title_text} {description_text}".lower()

        total_score = 0

        # Iterate through scoring rules
        for keyword, score in self.scoring_rules.items():
            if keyword in combined_text:
                total_score += score

        # Determine if article is considered a deal
        is_deal = total_score >= self.score_threshold

        return is_deal, total_score

    def filter_deal_articles(self, articles: list):
        """
        Filter list of articles keeping only deal-related ones.

        :param articles: List of keyword-filtered articles
        :return: List of confirmed deal articles
        """

        deal_articles = []

        for article in articles:
            is_deal, deal_score = self.classify_article(article)

            # Attach score for transparency/debugging
            article["deal_score"] = deal_score

            if is_deal:
                deal_articles.append(article)

        return deal_articles
