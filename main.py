import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to speak the assistant's response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to recognize and interpret user speech
def get_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"You said: {command}")
        except sr.UnknownValueError:
            command = ""
        return command.lower()

# Define a function to handle various user requests
def handle_request(command):
    if "reminder" in command:
        speak("What would you like me to remind you?")
        reminder_text = get_command()
        if reminder_text:
            speak("When would you like to be reminded? Please specify the time in HH:MM format.")
            time_text = get_command()
            if time_text:
                try:
                    time = datetime.datetime.strptime(time_text, "%H:%M").time()
                    now = datetime.datetime.now().time()
                    reminder_time = datetime.datetime.combine(datetime.date.today(), time)
                    if reminder_time < datetime.datetime.now():
                        reminder_time += datetime.timedelta(days=1)
                    delay = (reminder_time - datetime.datetime.now()).seconds
                    speak(f"Setting a reminder for {reminder_text} at {time_text}.")
                    os.system(f'sleep {delay}; say "Reminder: {reminder_text}" &')
                except ValueError:
                    speak("I'm sorry, I didn't understand the time you specified.")
            else:
                speak("I'm sorry, I didn't hear the time you specified.")
        else:
            speak("I'm sorry, I didn't hear what you wanted me to remind you.")
    elif "todo list" in command:
        speak("What task would you like to add to your to-do list?")
        task_text = get_command()
        if task_text:
            with open("todo.txt", "a") as f:
                f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {task_text}\n")
            speak(f"Added {task_text} to your to-do list.")
        else:
            speak("I'm sorry, I didn't hear what task you wanted to add to your to-do list.")
    elif "search" in command:
        speak("What would you like me to search for?")
        query_text = get_command()
        if query_text:
            url = f"https://www.google.com/search?q={query_text}"
            webbrowser.open_new_tab(url)
            speak(f"Here are the search results for {query_text}.")
        else:
            speak("I'm sorry, I didn't hear what you wanted me to search for.")
    else:
        speak("I'm sorry, I don't know how to do that yet.")

# Main loop to listen for and handle user requests
while True:
    command = get_command()
    handle_request(command)
