# This module removes duplicate defense deals coming from multiple news sources

from typing import List, Dict


class DealDeduplicator:
    """
    Deduplicates structured deals using strong business keys.
    """

    def deduplicate_deals(self, structured_deals: List[Dict]) -> List[Dict]:
        """
        Merge duplicate deals based on buyer, seller, and deal value.

        :param structured_deals: list of extracted deals
        :return: deduplicated deal list
        """

        unique_deals = []
        seen_signatures = set()

        for structured_deal in structured_deals:

            # Create strong signature for a deal
            deal_signature = self._build_signature(structured_deal)

            # Skip if already processed
            if deal_signature in seen_signatures:
                continue

            seen_signatures.add(deal_signature)
            unique_deals.append(structured_deal)

        return unique_deals

    # ------------------------------------------------------

    def _build_signature(self, structured_deal: Dict) -> str:
        """
        Build a unique identifier for a deal.

        Strong fields used:
        buyer + seller + deal_value_normalized

        :param structured_deal: deal dictionary
        :return: signature string
        """

        buyer_value = (structured_deal.get("buyer") or "").lower().strip()
        seller_value = (structured_deal.get("seller") or "").lower().strip()
        deal_value_value = str(structured_deal.get("deal_value_normalized") or "")

        signature = f"{buyer_value}|{seller_value}|{deal_value_value}"

        return signature
