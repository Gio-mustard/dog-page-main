API_KEY = "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"

from groq import Groq
import json

client = Groq(
    api_key=API_KEY,
)

MODEL = "llama3-70b-8192"

__get_prompt = lambda pattern :f"""

    Extract the {pattern}, and any extra details (e.g., medications, favorite color) from the following  description as a JSON object. Use the exact properties as specified ({pattern}, extra). Ensure all values are in the same language as the provided description (which may be in Spanish or other languages)."""+"""

    For "extra", format it as an array of objects or strings (e.g., {"title":..., "content":...}). If the content of an object is very short (10 characters or less), merge the title and content into a single string.
    """


def get_schema(description:str,pattern:str)->dict:
    prompt = __get_prompt(pattern)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}:{description}"
            }
        ],
        stop="```",
        temperature=0,
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)