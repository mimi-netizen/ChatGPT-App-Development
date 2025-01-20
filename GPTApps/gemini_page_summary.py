import requests
from bs4 import BeautifulSoup
import json

# Set the Gemini API key
gemini_api_key = ""

# Set the URL of the article to summarize
url = "https://en.wikipedia.org/wiki/Beautiful_demoiselle"

# Download the HTML content of the article
response = requests.get(url)
html = response.content

# Use BeautifulSoup to extract the main text of the article
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()

# Split the text into 3500-character chunks
chunks = [text[i:i+3500] for i in range(0, len(text), 3500)]

# Use the Gemini API to generate a summary for each chunk
summaries = []
chunks_count = 0
for chunk in chunks:
    prompt = f"Please summarize the following article in one sentence: {chunk}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    chunks_count += 1
    if response.status_code == 200:
        try:
            summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            summaries.append(summary)
        except (KeyError, IndexError):
            print(f"Gemini API Error: Unexpected response format for chunk {chunks_count}")
    else:
        print(f"Gemini API Error: {response.status_code} - {response.text}")

# Combine the summaries into a single text string
full_summary = "\n".join(summaries)

# Print the summary to the console
print(chunks_count)
print(full_summary)