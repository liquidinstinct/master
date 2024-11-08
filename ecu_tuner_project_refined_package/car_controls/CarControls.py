import pyttsx3
import can
import threading
import time

# Initialize TTS engine for voice feedback
tts_engine = pyttsx3.init()

# Function to handle TTS responses
def speak(message):
    tts_engine.say(message)
    tts_engine.runAndWait()

class CarControls:
    def __init__(self):
        # Initialize CAN bus and provide voice feedback
        speak("Advanced car control system initialized.")
        print("Advanced car control system initialized.")

        # Attempt to initialize CAN bus
        try:
            self.bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
            speak("CAN bus initialized.")
        except Exception as e:
            print("Error initializing CAN bus:", e)
            speak("Error initializing CAN bus.")
            self.bus = None

    # Window control example method
    def window_control(self, window, action):
        message = f"Rolling {action} the {window} window."
        speak(message)
        return {"status": "success", "message": message}

    # Start CAN sniffing in a background thread
    def start_sniffing_in_background(self, log_duration=10, save_to_file=True, filter_id=None):
        def sniff():
            start_time = time.time()
            log_file = open("logs/can_sniff.log", "w") if save_to_file else None
            speak("Starting CAN sniffing.")

            while time.time() - start_time < log_duration:
                msg = self.bus.recv(timeout=1)
                if msg and (filter_id is None or msg.arbitration_id == filter_id):
                    print(msg)
                    if save_to_file and log_file:
                        log_file.write(str(msg) + "\n")

            if log_file:
                log_file.close()
            speak("CAN sniffing completed.")

        # Start sniffing in a new thread
        sniffing_thread = threading.Thread(target=sniff, daemon=True)
        sniffing_thread.start()
