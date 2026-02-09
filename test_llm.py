from services.ollama_llm_extractor import OllamaLLMExtractor

llm = OllamaLLMExtractor()

text = "Enord secured a multi-crore Indian Army order for over 700 VR drone simulators."

print(llm.extract_json(text))
