import speech_recognition as sr
import yagmail

# Function to get user input for email addresses
def get_email_input(prompt):
    while True:
        email = input(prompt)
        if "@" in email and "." in email:
            return email
        else:
            print("Invalid email address. Please enter a valid email.")

# Speech Recognition
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print('Clearing background noise..')
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("waiting for your message...")
    recorded_audio = recognizer.listen(source)
    print('Done recording..!')

try:
    print('Printing the message..')
    text = recognizer.recognize_google(recorded_audio, language='en-US')
    print('Your message: {}'.format(text))
except Exception as ex:
    print(ex)
    text = "Speech recognition failed or no speech detected."

# Get user input for sender and receiver emails
sender_email = get_email_input("Enter your email address (sender): ")
receiver_email = get_email_input("Enter recipient's email address: ")

# Email Sending
message = text  # Make sure this line is properly indented

try:
    # Initialize yagmail.SMTP with authentication
    sender = yagmail.SMTP(sender_email)

    # Send email
    sender.send(to=receiver_email, subject='This is an automated mail', contents=message)
    print('Email sent successfully!')
except Exception as ex:
    print('Error sending email:', ex)
finally:
    # Close the connection
    sender.close()




