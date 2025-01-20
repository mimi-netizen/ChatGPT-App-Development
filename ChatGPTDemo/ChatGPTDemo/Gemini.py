import requests
import json

# Use Gemini API Key
gemini_api_key = "your_gemini_api_key_here"

# Ask the user for question
question = input("What would you like to ask the Gemini AI Assistant? ")

# Set up the API request
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + gemini_api_key
headers = {
    "Content-Type": "application/json"
}
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": question
                }
            ]
        }
    ]
}

# Send the API request and get the response
response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    try:
        # Extract the response content
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini AI Assistant: " + content)
    except (KeyError, IndexError):
        print("Gemini API Error: Unexpected response format")
else:
    print("Gemini API Error:", response.status_code, response.text)