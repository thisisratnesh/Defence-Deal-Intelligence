# This module normalizes deal values and quantities into clean numeric formats

import re


class ValueQuantityNormalizer:
    """
    Converts textual money values and quantities into numeric formats.
    """

    # -------------------- MONEY NORMALIZATION --------------------

    def normalize_deal_value(self, deal_value_raw, currency_raw):
        """
        Convert textual money value into integer amount.

        Example:
        "€140 million" -> 140000000
        "$165M" -> 165000000

        :param deal_value_raw: raw deal value text or number
        :param currency_raw: currency string
        :return: normalized integer or None
        """

        # If already numeric, return as is
        if isinstance(deal_value_raw, (int, float)):
            return int(deal_value_raw)

        if not deal_value_raw:
            return None

        text_value = str(deal_value_raw).lower()

        # Remove currency symbols and commas
        text_value = text_value.replace(",", "")
        text_value = re.sub(r"[€$£₹]", "", text_value)

        # ---------------- Handle billion ----------------

        if "billion" in text_value or "bn" in text_value:
            number_match = re.search(r"\d+(\.\d+)?", text_value)
            if number_match:
                return int(float(number_match.group()) * 1_000_000_000)

        # ---------------- Handle million ----------------

        if "million" in text_value or "m" in text_value:
            number_match = re.search(r"\d+(\.\d+)?", text_value)
            if number_match:
                return int(float(number_match.group()) * 1_000_000)

        # ---------------- Handle thousand ----------------

        if "thousand" in text_value or "k" in text_value:
            number_match = re.search(r"\d+(\.\d+)?", text_value)
            if number_match:
                return int(float(number_match.group()) * 1_000)

        # ---------------- Plain number ----------------

        number_match = re.search(r"\d+", text_value)
        if number_match:
            return int(number_match.group())

        return None

    # -------------------- QUANTITY NORMALIZATION --------------------

    def normalize_quantity(self, quantity_raw):
        """
        Convert textual quantity into integer.

        Example:
        "700+" -> 700
        "about 1,000 systems" -> 1000

        :param quantity_raw: raw quantity text
        :return: integer or None
        """

        if not quantity_raw:
            return None

        text_quantity = str(quantity_raw)

        # Remove commas
        text_quantity = text_quantity.replace(",", "")

        # Extract first number found
        number_match = re.search(r"\d+", text_quantity)

        if number_match:
            return int(number_match.group())

        return None
