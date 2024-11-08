import speech_recognition as sr
import pyttsx3
import requests  # For communicating with the backend
from datetime import datetime

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Set the TTS engine to use a male voice
def set_male_voice():
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if "male" in voice.name.lower() or "en-us" in voice.id.lower():
            tts_engine.setProperty('voice', voice.id)
            break
    tts_engine.setProperty('rate', 150)  # Adjust the speaking rate

set_male_voice()  # Call this to set to a male voice at the start

def listen_for_command():
    """
    Listens for a voice command through the default microphone.
    Returns:
        str: Transcribed text of the command, or error message.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)
        
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "Sorry, I didn't catch that."
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service; {e}")
        return "Error with the speech recognition service."

def speak(message):
    """
    Speaks the given message using TTS through the default audio output.
    Parameters:
        message (str): The message to speak out loud.
    """
    tts_engine.say(message)
    tts_engine.runAndWait()

def communicate_with_backend(endpoint, params=None):
    """
    Sends a request to the backend and retrieves a response.
    Parameters:
        endpoint (str): The endpoint to send the request to.
        params (dict): Optional query parameters for the request.
    Returns:
        str: Response text or error message.
    """
    base_url = "http://your-backend-server.com/api"  # Replace with your backend URL
    try:
        response = requests.get(f"{base_url}/{endpoint}", params=params)
        response.raise_for_status()
        data = response.json()  # Assuming the backend returns JSON
        return data.get("message", "No message received.")
    except requests.RequestException as e:
        print(f"Error communicating with backend: {e}")
        return "Error communicating with the backend service."

def handle_command(command):
    """
    Handles specific commands and performs actions based on recognized phrases.
    Parameters:
        command (str): The transcribed text of the command.
    """
    if "hello" in command:
        speak("Hello! How can I help you today?")
    elif "time" in command:
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        today_date = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today_date}.")
    elif "weather" in command:
        # Example command that interacts with backend
        location = "New Zealand"  # This could be dynamically parsed from the command
        response_message = communicate_with_backend("weather", params={"location": location})
        speak(response_message)
    elif "news" in command:
        # Another example for backend interaction
        response_message = communicate_with_backend("latest-news")
        speak(response_message)
    elif "exit" in command or "quit" in command:
        speak("Exiting voice command mode.")
        return True  # Return True to signal the main loop to exit
    else:
        speak("Command not recognized. Please try again.")
    return False

# Main loop to handle voice commands
if __name__ == "__main__":
    while True:
        command = listen_for_command()
        if handle_command(command):
            break

    
