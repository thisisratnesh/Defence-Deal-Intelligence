# This module extracts and cleans JSON from raw LLM output text

import json
import re


class LLMJsonCleaner:
    """
    Cleans and validates structured JSON produced by LLM.
    """

    def extract_json_from_text(self, raw_llm_output: str):
        """
        Extract first JSON block found inside text.

        :param raw_llm_output: Raw text produced by LLM
        :return: Parsed dictionary or None
        """

        try:
            # Find first opening and last closing curly braces
            start_index = raw_llm_output.find("{")
            end_index = raw_llm_output.rfind("}")

            # If no JSON-like structure found
            if start_index == -1 or end_index == -1:
                return None

            # Extract JSON substring
            json_string = raw_llm_output[start_index:end_index + 1]

            # Parse into Python dictionary
            parsed_json = json.loads(json_string)

            return parsed_json

        except Exception as error:
            print(f"JSON extraction failed: {error}")
            return None

    def normalize_deal_fields(self, extracted_json: dict):
        """
        Apply logical cleanup and validation rules.

        :param extracted_json: Raw parsed JSON from LLM
        :return: Clean structured deal dictionary
        """

        if extracted_json is None:
            return None

        # Extract fields safely
        buyer = extracted_json.get("buyer")
        seller = extracted_json.get("seller")
        product = extracted_json.get("product")
        quantity = extracted_json.get("quantity")
        deal_value = extracted_json.get("deal_value")
        currency = extracted_json.get("currency")
        deal_date = extracted_json.get("deal_date")

        # -------- Field correction rules -------- #

        # Swap buyer and seller if military is wrongly placed
        if buyer and "army" in buyer.lower():
            buyer, seller = seller, buyer

        # Normalize currency
        if currency:
            if "rupee" in currency.lower():
                currency = "INR"
            elif "dollar" in currency.lower():
                currency = "USD"

        # Quantity should be numeric (extract digits if present)
        if quantity:
            numeric_match = re.search(r"\d+", str(quantity))
            if numeric_match:
                quantity = numeric_match.group()
            else:
                quantity = None

        # Deal value should contain money words
        if deal_value and isinstance(deal_value, str):
            if "crore" not in deal_value.lower() and "million" not in deal_value.lower():
                deal_value = None

        # Remove hallucinated dates
        if deal_date and deal_date == "2021-01-01":
            deal_date = None

        # Build clean structured deal
        cleaned_deal = {
            "buyer": buyer,
            "seller": seller,
            "product": product,
            "quantity": quantity,
            "deal_value": deal_value,
            "currency": currency,
            "deal_date": deal_date
        }

        return cleaned_deal
