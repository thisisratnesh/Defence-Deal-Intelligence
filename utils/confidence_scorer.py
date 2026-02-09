# This module calculates confidence score for extracted defense deals

import re


class ConfidenceScorer:
    """
    Assigns confidence score to structured deal data
    based on presence of strong real-world signals.
    """

    def calculate_confidence(self, structured_deal: dict) -> float:
        """
        Compute confidence score from 0.0 to 1.0

        :param structured_deal: extracted deal dictionary
        :return: confidence score float
        """

        # ---------------- Base confidence ----------------

        confidence_score = 0.3

        # ---------------- Strong numeric signals ----------------

        # Boost if deal value exists
        if structured_deal.get("deal_value"):
            confidence_score += 0.2

        # Boost if quantity exists
        if structured_deal.get("quantity"):
            confidence_score += 0.2

        # ---------------- Entity presence ----------------

        # Boost if buyer detected
        if structured_deal.get("buyer"):
            confidence_score += 0.1

        # Boost if seller detected
        if structured_deal.get("seller"):
            confidence_score += 0.1

        # Boost if product detected
        if structured_deal.get("product"):
            confidence_score += 0.05

        # ---------------- Number in summary ----------------

        summary_text = structured_deal.get("summary", "")

        # Regex check for any digit in summary
        if re.search(r"\d", summary_text):
            confidence_score += 0.05

        # ---------------- Clamp to 1.0 ----------------

        if confidence_score > 1.0:
            confidence_score = 1.0

        return round(confidence_score, 2)
