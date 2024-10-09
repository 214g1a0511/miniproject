import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import smtplib
from email.message import EmailMessage

class EmailVoiceAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Voice Assistant")
        self.geometry("400x350")

        self.sender_label = tk.Label(self, text="Sender Email:")
        self.sender_label.pack()
        self.sender_entry = tk.Entry(self)
        self.sender_entry.pack()

        self.sender_password_label = tk.Label(self, text="Sender Password:")
        self.sender_password_label.pack()
        self.sender_password_entry = tk.Entry(self, show="*")
        self.sender_password_entry.pack()

        self.receiver_label = tk.Label(self, text="Receiver Email:")
        self.receiver_label.pack() 
        self.receiver_entry = tk.Entry(self)
        self.receiver_entry.pack()

        self.subject_label = tk.Label(self, text="Subject:")
        self.subject_label.pack()

        self.subject_record_button = tk.Button(self, text="Record Subject", command=self.record_subject)
        self.subject_record_button.pack()

        self.subject_audio_label = tk.Label(self, text="Subject Audio:")
        self.subject_audio_label.pack()
        self.subject_audio_display = tk.Entry(self, state="disabled")
        self.subject_audio_display.pack()

        self.content_label = tk.Label(self, text="Content:")
        self.content_label.pack()

        self.content_record_button = tk.Button(self, text="Record Content", command=self.record_content)
        self.content_record_button.pack()

        self.content_audio_label = tk.Label(self, text="Content Audio:")
        self.content_audio_label.pack()
        self.content_audio_display = tk.Entry(self, state="disabled")
        self.content_audio_display.pack()

        self.send_button = tk.Button(self, text="Send Email", command=self.send_email)
        self.send_button.pack()

        self.subject_audio = None
        self.content_audio = None

    def record_subject(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Record", "Recording Subject...")
            audio = recognizer.listen(source)
            try:
                self.subject_audio = recognizer.recognize_google(audio)
                self.subject_audio_display.config(state="normal")
                self.subject_audio_display.delete(0, tk.END)
                self.subject_audio_display.insert(tk.END, self.subject_audio)
                self.subject_audio_display.config(state="disabled")
                messagebox.showinfo("Record", "Subject Recorded Successfully")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results")

    def record_content(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Record", "Recording Content...")
            audio = recognizer.listen(source)
            try:
                self.content_audio = recognizer.recognize_google(audio)
                self.content_audio_display.config(state="normal")
                self.content_audio_display.delete(0, tk.END)
                self.content_audio_display.insert(tk.END, self.content_audio)
                self.content_audio_display.config(state="disabled")
                messagebox.showinfo("Record", "Content Recorded Successfully")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results")

    def send_email(self):
        if self.subject_audio is None or self.content_audio is None:
            messagebox.showerror("Error", "Please record both subject and content")
            return

        sender_email = self.sender_entry.get()
        sender_password = self.sender_password_entry.get()
        receiver_email = self.receiver_entry.get()

        msg = EmailMessage()
        msg.set_content(f"{self.content_audio}")

        # Assign recorded subject to email subject
        msg['Subject'] = self.subject_audio
        
        # Add your email details
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        # Add your SMTP server details
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        messagebox.showinfo("Success", "Email Sent Successfully")

if __name__ == "__main__":
    app = EmailVoiceAssistant()
    app.mainloop()




