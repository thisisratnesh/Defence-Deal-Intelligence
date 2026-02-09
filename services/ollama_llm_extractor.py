from langchain_ollama import OllamaLLM


class OllamaLLMExtractor:
    def __init__(self, model_name="llama3"):
        self.llm = OllamaLLM(model=model_name)

    def extract_json(self, article_text: str):
        prompt = f"""
Return STRICT JSON only with:

buyer, seller, product, quantity, deal_value, currency, deal_date, summary

Text:
{article_text}
"""
        return self.llm.invoke(prompt)
