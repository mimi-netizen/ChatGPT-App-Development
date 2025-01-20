import win32com.client
import tkinter as tk
from tkinter import ttk
import requests
import json

gemini_api_key = "your_gemini_api_key_here"

def last_10_emails():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    emails = [messages.GetLast().Subject]
    email_number = 10
    for i in range(email_number):
        emails.append(messages.GetPrevious().Subject)
    return emails

def reply():
    email = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI").\
        GetDefaultFolder(6).Items.Item(selected_subject.get())
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Create a reply to this email:\n{email.Body}"
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            reply_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            reply = email.Reply()
            reply.Body = reply_text
            reply.Display()
        except (KeyError, IndexError):
            print("Gemini API Error: Unexpected response format")
    else:
        print(f"Gemini API Error: {response.status_code} - {response.text}")

root = tk.Tk()
root.title("Outlook Emails")

# Set up styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#4267B2", foreground="white", font=("Arial", 12, "bold"))
style.configure("TLabel", background="#f4f4f4", foreground="#333333", font=("Open Sans", 14))
style.configure("TOptionMenu", background="white", foreground="#333333", font=("Arial", 12))

# Set up the UI
root.configure(bg="#f4f4f4")

email_subjects = last_10_emails()
selected_subject = tk.StringVar()

dropdown = ttk.OptionMenu(root, selected_subject, *email_subjects)
dropdown.pack(pady=10)

label = ttk.Label(root, text="")
label.pack(pady=10)

button = ttk.Button(root, text="Generate Reply", command=reply, style="TButton")
button.pack(pady=10)

root.mainloop()