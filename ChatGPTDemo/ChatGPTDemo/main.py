import openai

# Use OpenAI API Key
openai.api_key = "your_api_key_here"

# Ask the user for question
question = input("What would you like to ask OpenAI? ")

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=question,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.8,
)

answer = response["choices"][0]["text"]

print("OpenAI: " + str(response))