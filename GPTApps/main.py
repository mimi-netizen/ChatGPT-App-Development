from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = "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"


# Define a function to generate business name ideas
def generate_business_names(prompt):
    model_engine = "text-davinci-003"
    prompt = (
        f"Generate 10 business name ideas based on the description: '{prompt}'\n"
        f"1. \n2. \n3. \n4. \n5. \n6. \n7. \n8. \n9. \n10.")
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    ideas = response.choices[0].text.strip().split("\n")[1:]
    return ideas


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
