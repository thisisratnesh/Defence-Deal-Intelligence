# Offline LLM structured extraction using HuggingFace transformers

from transformers import pipeline


class LocalLLMExtractor:
    """
    Offline LLM based structured deal extractor.
    """

    def __init__(self, model_name: str):
        """
        Load pretrained HuggingFace model locally.

        :param model_name: HuggingFace model identifier
        """

        # Use supported pipeline type (works across versions)
        self.extractor = pipeline(
            "text-generation",
            model=model_name
        )

    def extract_structured_deal(self, article: dict):
        """
        Extract structured deal info from article text.

        :param article: Deal-related article dictionary
        :return: Structured deal dictionary
        """

        article_title = article.get("title", "")
        article_description = article.get("seendescription", "")
        article_url = article.get("url", "")

        combined_text = f"{article_title} {article_description}"

        prompt = f"""
Extract deal details in JSON.

Fields:
buyer, seller, product, quantity, deal_value, currency, deal_date

Text:
{combined_text}

JSON:
"""

        try:
            response = self.extractor(
                prompt,
                max_new_tokens=200,
                do_sample=False
            )

            generated_text = response[0]["generated_text"]

            structured_deal = {
                "buyer": "PENDING",
                "seller": "PENDING",
                "product": "PENDING",
                "quantity": "PENDING",
                "deal_value": "PENDING",
                "currency": "PENDING",
                "deal_date": "PENDING",
                "source_url": article_url,
                "raw_llm_output": generated_text
            }

            return structured_deal

        except Exception as error:
            print(f"LLM extraction failed: {error}")

            return {
                "buyer": "FAILED",
                "seller": "FAILED",
                "product": "FAILED",
                "quantity": "FAILED",
                "deal_value": "FAILED",
                "currency": "FAILED",
                "deal_date": "FAILED",
                "source_url": article_url
            }
