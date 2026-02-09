# This class runs a pretrained HuggingFace LLM locally for structured extraction

from transformers import pipeline


class LocalLLMExtractor:
    """
    Offline LLM based structured deal extractor using HuggingFace models.
    """

    def __init__(self, model_name: str):
        """
        Load pretrained model locally.

        :param model_name: HuggingFace model identifier
        """

        # Create text generation pipeline
        self.generator = pipeline(
            "text-generation",
            model=model_name,
            device_map="auto"
        )

    def extract_structured_deal(self, article: dict):
        """
        Extract structured deal info using local LLM.

        :param article: Deal-related article dictionary
        :return: Structured deal dictionary
        """

        article_title = article.get("title", "")
        article_description = article.get("seendescription", "")
        article_url = article.get("url", "")

        combined_text = f"{article_title} {article_description}"

        # Prompt carefully designed for structured extraction
        prompt = f"""
Extract deal information from the text below.

Return JSON with keys:
buyer, seller, product, quantity, deal_value, currency, deal_date

Text:
{combined_text}
"""

        try:
            # Generate model output
            response = self.generator(
                prompt,
                max_new_tokens=200,
                do_sample=False
            )

            generated_text = response[0]["generated_text"]

            # For now return raw output (later we’ll clean JSON properly)
            structured_deal = {
                "buyer": "PARSING_PENDING",
                "seller": "PARSING_PENDING",
                "product": "PARSING_PENDING",
                "quantity": "PARSING_PENDING",
                "deal_value": "PARSING_PENDING",
                "currency": "PARSING_PENDING",
                "deal_date": "PARSING_PENDING",
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
