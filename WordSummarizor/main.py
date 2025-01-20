import openai
import docx
import tkinter as tk
from tkinter import filedialog


def summarize_text(file_location):
    doc = docx.Document(file_location)
    text = ""
    for para in doc.paragraphs:
        text += para.text

    openai.api_key = "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"
    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine=model_engine,
        prompt="Summarize the following text in two sentences: \n"
               + '" ' + text + ' "',
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
    )
    summarized_text = response["choices"][0]["text"]

    return summarized_text


root = tk.Tk()
root.title("Text Summarizer")
root.configure(bg="white")

header_font = ("Open Sans", 16, "bold")

header = tk.Label(root,
                  text="Text Summarizer",
                  bg="white",
                  font=header_font,
                  )

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


browse_button = tk.Button(root, text="Browse", command=browse_file,
                          bg="#4267B2", fg="black", relief="flat",
                          borderwidth=0, activebackground="#4267B2",
                          activeforeground="white")

browse_button.config(font=("Arial", 12, "bold"), width=10, height=2)
browse_button.pack()
text_field = tk.Text(root, height=20, width=50, bg="white", fg="black",
                     relief="flat", borderwidth=0)

text_field.pack()

root.mainloop()
