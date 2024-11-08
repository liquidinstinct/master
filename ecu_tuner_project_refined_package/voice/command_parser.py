
       
import speech_recognition as sr
import pyttsx3
from app import read_data, read_fault_codes
from ecu_handlers.obd2_handler import OBD2Handler
from ecu_handlers.haltech_handler import HaltechHandler
from ecu_handlers.gpt_handler import analyze_fault_codes_with_gpt

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

set_male_voice()  # Set the voice at the start

def listen_for_command():
    """Listens for a voice command and returns transcribed text or error."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)
        
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        speak("Speech recognition service is unavailable.")
        return None

def speak(message):
    """Speaks the provided message."""
    tts_engine.say(message)
    tts_engine.runAndWait()

# Command Parser
def parse_command(command, obd_handler):
    """Parses a command and executes corresponding action with ECU handler."""
    if not command:
        return
    
    if "check connection" in command:
        check_connection(obd_handler) # type: ignore
    elif "read rpm" in command:
        read_data("rpm", obd_handler)
    elif "read speed" in command:
        read_data("speed", obd_handler)
    elif "engine temperature" in command:
        read_data("engine_temp", obd_handler)
    elif "fuel level" in command:
        read_data("fuel_level", obd_handler)
    elif "throttle position" in command:
        read_data("throttle_position", obd_handler)
    elif "battery voltage" in command:
        read_data("battery_voltage", obd_handler)
    elif "fault codes" in command and "clear" in command:
        read_fault_codes(obd_handler)
    elif "fault codes" in command or "error codes" in command:
        read_fault_codes(obd_handler)
    
