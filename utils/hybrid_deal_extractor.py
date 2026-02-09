import re
from utils.llm_json_cleaner import LLMJsonCleaner


class HybridDealExtractor:
    """
    Hybrid extractor that extracts structured fields when possible,
    or at least generates a useful summary containing numbers if not.
    """

    def __init__(self):
        self.json_cleaner = LLMJsonCleaner()

    def extract_numbers(self, text: str):
        """
        Extract all numbers from text (including units like million/billion/crore).
        """
        # Find sequences like 720, 50-60, $200, 1000m, etc.
        matches = re.findall(r"\d+(?:[-–]\d+)?(?:\s?(million|billion|crore|m|bn))?", text, flags=re.IGNORECASE)

        # Flatten non-empty matches and return as list of unique numeric strings
        cleaned = [m[0] if isinstance(m, tuple) and m[0] else m for m in matches]
        return cleaned if cleaned else None

    def extract_deal_value(self, text: str):
        """
        Extract deal value related to money expressions like
        'multi-crore', '$200 million', '₹500 crore', '150M', etc.
        """
        money_match = re.search(
            r"(\$|₹|€)?\s?\d+(?:\s?(million|billion|crore|m|bn))",
            text,
            flags=re.IGNORECASE
        )
        if money_match:
            return money_match.group(0)
        if "multi-crore" in text.lower():
            return "multi-crore"
        return None

    def generate_summary(self, title: str, raw_text: str, numbers: list):
        """
        Generate fallback summary (including numeric info).
        """
        # Base summary
        summary = f"{title.strip()}. "

        # Add contextual numeric details, if any
        if numbers:
            summary += "Contains numbers: " + ", ".join(numbers) + "."

        return summary

    def process_article(self, structured_deal_raw: dict):
        """
        Master hybrid extraction function.

        Returns either a structured deal or at least a fallback
        summary with numeric indicators.
        """

        raw_llm_output = structured_deal_raw.get("raw_llm_output", "")
        source_url = structured_deal_raw.get("source_url", "")
        title_text = structured_deal_raw.get("title", "")
        raw_text = structured_deal_raw.get("raw_text", "")

        # ---- Attempt structured extraction ----
        extracted_json = self.json_cleaner.extract_json_from_text(raw_llm_output)
        cleaned_deal = self.json_cleaner.normalize_deal_fields(extracted_json)

        # ---- Post-process to fill missing numeric info ----
        if cleaned_deal:

            # Attempt to extract quantity from text
            numbers = self.extract_numbers(raw_text)
            deal_value = self.extract_deal_value(raw_text)

            if numbers:
                cleaned_deal["quantity"] = numbers[0]

            if deal_value:
                cleaned_deal["deal_value"] = deal_value

            cleaned_deal["source_url"] = source_url
            cleaned_deal["summary"] = self.generate_summary(
                title_text, raw_text, numbers
            )
            cleaned_deal["confidence"] = 0.8

            return cleaned_deal

        # ---- Fallback partial summary (structured deal failed) ----

        # Extract any numbers at least
        numbers = self.extract_numbers(raw_text)

        # Build fallback summary text
        fallback_summary = self.generate_summary(
            title_text,
            raw_text,
            numbers
        )

        return {
            "source_url": source_url,
            "summary": fallback_summary,
            "confidence": 0.25
        }
