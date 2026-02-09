import json


def parse_llm_json(raw_text: str):
    """
    Safely extract JSON from LLM response.
    """

    try:
        start = raw_text.find("{")
        end = raw_text.rfind("}")

        if start == -1 or end == -1:
            return None

        json_string = raw_text[start:end + 1]

        return json.loads(json_string)

    except Exception as error:
        print(f"JSON parsing failed: {error}")
        return None
