from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Set up Gemini API credentials
gemini_api_key = ""


# Define a function to generate business name ideas
def generate_business_names(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Generate 10 business name ideas based on the description: '{prompt}'\n1.\n2.\n3.\n4.\n5.\n6.\n7.\n8.\n9.\n10."
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            ideas = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip().split("\n")[1:]
            return ideas
        except (KeyError, IndexError):
            print("Gemini API Error: Unexpected response format")
            return []
    else:
        print(f"Gemini API Error: {response.status_code} - {response.text}")
        return []


# Define a route to display a form for the user to input their business
# description
@app.route("/")
def index():
    return render_template("index.html")


# Define a route to handle the form submission and display the generated
# business name ideas
@app.route("/", methods=["POST"])
def generate():
    prompt = request.form["description"]
    names = generate_business_names(prompt)
    print(names)
    return render_template("index.html", names=names)


if __name__ == "__main__":
    app.run(debug=True)