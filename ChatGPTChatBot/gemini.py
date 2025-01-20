from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

# Use your Gemini API key
gemini_api_key = "AIzaSyAAadKS6jNSX_s_1KadF1oyF6g7cXTOAfs"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')

    # Set up the Gemini API request
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + gemini_api_key
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_text
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
            return str(content)
        except (KeyError, IndexError):
            return "Gemini API Error: Unexpected response format"
    else:
        return "Gemini API Error: " + str(response.status_code) + " - " + response.text

if __name__ == "__main__":
    app.run()