import openai
import json
from pathlib import Path

PROMPT = "3D render of a futuristic castle in a clear sky, digital art"
DATA_DIRECTORY = Path.cwd() / "responses"

DATA_DIRECTORY.mkdir(exist_ok=True)

openai.api_key = "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"

response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="1024x1024",
    response_format="b64_json"
)

file_name = DATA_DIRECTORY / f"{PROMPT[:5]}-{response['created']}.json"

with open(file_name, mode='w', encoding="utf-8") as file:
    json.dump(response, file)
