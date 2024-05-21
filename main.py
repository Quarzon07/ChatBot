import tkinter as tk
from tkinter import scrolledtext
import json
import tkinter.simpledialog as simpledialog

class ChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("400x500")

        self.language = 'it'
        self.responses_db = self.load_responses(self.language)

        self.chat_log = scrolledtext.ScrolledText(self.root, width=40, height=20)
        self.chat_log.pack(padx=10, pady=10)

        self.input_field = tk.Entry(self.root, width=30)
        self.input_field.pack(padx=10, pady=10)
        self.input_field.bind('<Return>', self.send_message)

        self.send_button = tk.Button(self.root, text="Invia", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.chat_log.insert(tk.INSERT, "Ciao, sono il tuo chatbot personale!\n")

    def load_responses(self, language):
        with open(f'responses_{language}.json', 'r') as f:
            responses = json.load(f)
        return responses

    def get_response(self, input_text):
        input_text = input_text.lower()
        responses_db = self.responses_db

        for keyword, response in responses_db.items():
            if keyword in input_text:
                return response
        return "Mi dispiace, non capisco."

    def learn_new_response(self, user_input, new_response):
        responses_db = self.responses_db
        responses_db[user_input] = new_response
        with open(f'responses_{self.language}.json', 'w') as f:
            json.dump(responses_db, f)

    def send_message(self, event=None):
        user_input = self.input_field.get()
        response = self.get_response(user_input)
        self.chat_log.insert(tk.INSERT, f"User: {user_input}\n")
        self.chat_log.insert(tk.INSERT, f"ChatBot: {response}\n")

        if response == "Mi dispiace, non capisco.":
            self.chat_log.insert(tk.INSERT, "ChatBot: Insegnami una nuova parola chiave e la sua risposta.\n")

            new_keyword = simpledialog.askstring("Nuova parola chiave", "Inserisci la nuova parola chiave:")
            if new_keyword:
                new_response = simpledialog.askstring("Nuova risposta", f"Inserisci la risposta per '{new_keyword}':")
                if new_response:
                    self.learn_new_response(new_keyword, new_response)
                    self.chat_log.insert(tk.INSERT, f"ChatBot: Ho imparato la nuova risposta '{new_response}' per '{new_keyword}'.\n")

        self.input_field.delete(0, tk.END)

root = tk.Tk()
chatbot = ChatBot(root)
root.mainloop()
