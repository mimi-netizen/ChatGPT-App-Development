import requests
from bs4 import BeautifulSoup
import openai
openai.api_key = "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"

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

# Use the OpenAI API to generate a summary for each chunk
summaries = []
model = "text-davinci-003"
chunks_count = 0
for chunk in chunks:
    prompt = f"Please summarize the following article in one sentence: {chunk}"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=200,
        n=1,
        stop=None,
    )
    chunks_count += 1
    summary = response.choices[0].text
    summaries.append(summary)

# Combine the summaries into a single text string
full_summary = "\n".join(summaries)

# Print the summary to the console
print(chunks_count)
print(full_summary)