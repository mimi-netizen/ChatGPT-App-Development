from flask import Flask, request, render_template
import hashlib
import sqlite3
import stripe
import requests
import json

app = Flask(__name__)

# Gemini API Key
gemini_api_key = "your api key"

# Stripe API Key
stripe.api_key = "your stripe key"

def initialize_database():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (fingerprint text primary key, usage_counter int)''')
    conn.commit()
    conn.close()

def get_fingerprint():
    browser = request.user_agent.browser
    version = request.user_agent.version and float(
        request.user_agent.version.split(".")[0])
    platform = request.user_agent.platform
    string = f"{browser}:{version}:{platform}"
    fingerprint = hashlib.sha256(string.encode("utf-8")).hexdigest()
    return fingerprint

def get_usage_counter(fingerprint):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users '
              '(fingerprint text, usage_counter int)')
    result = c.execute('SELECT usage_counter FROM users WHERE fingerprint=?',
                       [fingerprint]).fetchone()
    conn.close()
    if result is None:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (fingerprint, usage_counter) VALUES '
                  '(?, 0)', [fingerprint])
        conn.commit()
        conn.close()
        return 0
    else:
        return result[0]

def update_usage_counter(fingerprint, usage_counter):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('UPDATE users SET usage_counter=? WHERE fingerprint=?',
              [usage_counter, fingerprint])
    conn.commit()
    conn.close()

def process_code_with_gemini(code, error):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + gemini_api_key
    headers = {"Content-Type": "application/json"}

    # Get explanation
    explanation_data = {
        "contents": [{
            "parts": [{
                "text": f"Explain the error in this code without fixing it:\n\n{code}\n\nError:\n\n{error}"
            }]
        }]
    }
    explanation_response = requests.post(url, headers=headers, data=json.dumps(explanation_data))
    
    if explanation_response.status_code == 200:
        try:
            explanation = explanation_response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            explanation = "Gemini API Error: Unexpected response format"
    else:
        explanation = f"Gemini API Error: {explanation_response.status_code} - {explanation_response.text}"

    # Get fixed code
    fix_data = {
        "contents": [{
            "parts": [{
                "text": f"Fix this code:\n\n{code}\n\nError:\n\n{error}. Respond only with the fixed code."
            }]
        }]
    }
    fix_response = requests.post(url, headers=headers, data=json.dumps(fix_data))
    
    if fix_response.status_code == 200:
        try:
            fixed_code = fix_response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            fixed_code = "Gemini API Error: Unexpected response format"
    else:
        fixed_code = f"Gemini API Error: {fix_response.status_code} - {fix_response.text}"

    return explanation, fixed_code

@app.route("/", methods=["GET", "POST"])
def index():
    initialize_database()
    fingerprint = get_fingerprint()
    usage_counter = get_usage_counter(fingerprint)

    if request.method == "POST":
        code = request.form["code"]
        error = request.form["error"]
        
        # Process the request first
        explanation, fixed_code = process_code_with_gemini(code, error)
        
        # Increment counter after processing
        usage_counter += 1
        update_usage_counter(fingerprint, usage_counter)
        
        # If this was their first use (counter is now 1), or they've paid
        if usage_counter <= 1:
            return render_template("index.html",
                                 explanation=explanation,
                                 fixed_code=fixed_code,
                                 usage_counter=usage_counter)
        # If they've used it more than once but haven't paid
        elif usage_counter > 3:
            return render_template("payment.html",
                                 explanation=explanation,
                                 fixed_code=fixed_code)
        else:
            return render_template("index.html",
                                 explanation=explanation,
                                 fixed_code=fixed_code,
                                 usage_counter=usage_counter)

    return render_template("index.html", usage_counter=usage_counter)

@app.route("/charge", methods=["POST"])
def charge():
    amount = int(request.form["amount"])
    plan = str(request.form["plan"])

    customer = stripe.Customer.create(
        email=request.form["stripeEmail"],
        source=request.form["stripeToken"]
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency="usd",
        description="App Charge"
    )

    return render_template("charge.html", amount=amount, plan=plan)

if __name__ == "__main__":
    app.run()