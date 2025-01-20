import openai
import win32com.client
import tkinter as tk

openai.api_key = "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"


def last_10_emails():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    emails = [messages.GetLast().Subject]
    email_number = 10
    for i in range(email_number):
        emails.append(messages.GetPrevious().Subject)
    return emails


root = tk.Tk()
root.title("Outlook Emails")
root.geometry("300x300")

email_subjects = last_10_emails()
selected_subject = tk.StringVar()

dropdown = tk.OptionMenu(root, selected_subject, *email_subjects)
dropdown.pack()

label = tk.Label(root, text="")
label.pack()

def reply():
    email = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI").\
        GetDefaultFolder(6).Items.Item(selected_subject.get())
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Create a reply to this email:\n" + email.Body,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.8,
    )

    reply = email.Reply()
    reply.Body = response["choices"][0]["text"]

    reply.Display()
    return


button = tk.Button(root, text="Generate Reply",
                   command=reply)
button.pack()

root.mainloop()
