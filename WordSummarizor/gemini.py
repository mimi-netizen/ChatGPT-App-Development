import docx
import tkinter as tk
from tkinter import filedialog
import requests
import json
from tkinter import ttk

def summarize_text(file_location):
    doc = docx.Document(file_location)
    text = ""
    for para in doc.paragraphs:
        text += para.text

    gemini_api_key = "your_gemini_api_key_here"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Summarize the following text in two sentences:\n\"{text}\""
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            summarized_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return summarized_text
        except (KeyError, IndexError):
            print("Gemini API Error: Unexpected response format")
            return ""
    else:
        print(f"Gemini API Error: {response.status_code} - {response.text}")
        return ""


root = tk.Tk()
root.title("Text Summarizer")
root.configure(bg="#f4f4f4")

# Set up styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#4267B2", foreground="white", font=("Arial", 12, "bold"))
style.configure("TLabel", background="#f4f4f4", foreground="#333333", font=("Open Sans", 14))
style.configure("TText", background="white", foreground="#333333", font=("Arial", 12))

header_font = ("Open Sans", 18, "bold")

header = ttk.Label(root,
                  text="Text Summarizer",
                  style="TLabel")

header.pack(pady=20)

def browse_file():
    file_location = filedialog.askopenfilename(initialdir="/",
                                               title="Select file",
                                               filetypes=
                                               (("Word files", "*.docx"),
                                                ("all files", "*.*")))
    if file_location:
        summarized_text = summarize_text(file_location)
        text_field.delete("1.0", tk.END)
        text_field.insert(tk.END, summarized_text)

browse_button = ttk.Button(root, text="Browse", command=browse_file,
                          style="TButton")

browse_button.pack(pady=10)

text_field = tk.Text(root, height=20, width=60, bg="white", fg="#333333",
                     relief="flat", borderwidth=0, font=("Arial", 12))

text_field.pack(pady=10)

root.mainloop()