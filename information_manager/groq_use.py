API_KEY = "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"

from groq import Groq
import json

client = Groq(
    api_key=API_KEY,
)

MODEL = "llama3-70b-8192"

def __get_promt()->str:
    with open('information_manager/prompt_to_get_schema.txt', 'r',encoding='utf8') as file:
        return file.read()


def get_schema(description:str)->dict:
    prompt = __get_promt()
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