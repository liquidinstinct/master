import os
import openai
import pyttsx3

# Initialize TTS engine for voice feedback
tts_engine = pyttsx3.init()

# Set up OpenAI API Key
openai.api_key = os.getenv(

# Function to handle TTS responses
def speak(message):
    tts_engine.say(message)
    tts_engine.runAndWait()

def analyze_fault_codes_with_gpt(fault_codes):
    """
    Use GPT-4 to analyze provided fault codes and generate diagnostic suggestions.
    Parameters:
    - fault_codes: str, a comma-separated string of fault codes (e.g., "P0171, P0301")
    
    Returns a structured response with analysis and suggestions.
    """
    # GPT-4 prompt to analyze fault codes
    prompt = (
        f"The following fault codes were retrieved from the vehicle: {fault_codes}. "
        "Provide a detailed diagnostic analysis for each code, including possible causes, "
        "suggested actions, and any relevant troubleshooting tips. "
        "If any code is unknown, indicate that and suggest a general approach to diagnostics."
    )

    try:
        # Call the GPT-4 API
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )
        analysis = response.choices[0].text.strip()

        # Provide TTS feedback
        speak("Diagnostic analysis completed.")
        return {"status": "success", "analysis": analysis}
    
    except Exception as e:
        error_message = "Error generating GPT analysis."
        speak(error_message)
        return {"status": "error", "message": error_message, "details": str(e)}

def gpt_process_command(command, car_controls):
    """
    Process a general command using GPT-4 and perform specific car control actions.
    Parameters:
    - command: str, the voice command to process
    - car_controls: CarControls instance to execute vehicle-specific commands
    """
    command = command.lower()  # Normalize command text

    # Map common commands directly to car control functions if detected
    if "window" in command:
        if "up" in command or "close" in command:
            return car_controls.window_control("all", "up")
        elif "down" in command or "open" in command:
            return car_controls.window_control("all", "down")
    
    elif "air conditioning" in command or "AC" in command:
        if "on" in command:
            return car_controls.ac_control("on")
        elif "off" in command:
            return car_controls.ac_control("off")
        elif "increase" in command:
            return car_controls.ac_control("increase")
        elif "decrease" in command:
            return car_controls.ac_control("decrease")
        # Attempt to parse a specific temperature if mentioned
        temp_words = [int(s) for s in command.split() if s.isdigit()]
        if temp_words:
            temperature = temp_words[0]
            return car_controls.ac_control("set", temperature)

    elif "media" in command:
        if "play" in command:
            return car_controls.media_control("play")
        elif "pause" in command:
            return car_controls.media_control("pause")
        elif "next" in command:
            return car_controls.media_control("next")
        elif "previous" in command:
            return car_controls.media_control("previous")
        elif "volume up" in command:
            return car_controls.media_control("volume up")
        elif "volume down" in command:
            return car_controls.media_control("volume down")

    elif "light" in command:
        if "headlight" in command:
            if "on" in command:
                return car_controls.light_control("headlights", "on")
            elif "off" in command:
                return car_controls.light_control("headlights", "off")
        elif "interior" in command:
            if "dim" in command:
                return car_controls.light_control("interior", "dim")
            elif "bright" in command:
                return car_controls.light_control("interior", "bright")

    # If no specific function matches, pass the command to GPT-4 for general processing
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=f"The user gave this command: '{command}'. What action should be taken?",
            max_tokens=150,
            temperature=0.5
        )
        gpt_response = response.choices[0].text.strip()
        speak(gpt_response)
        return {"status": "success", "response": gpt_response}

    except Exception as e:
        error_message = "Error processing command with GPT."
        speak(error_message)
        return {"status": "error", "message": error_message, "details": str(e)}

# Example usage of the functions
if __name__ == "__main__":
    # Simulating fault code analysis
    print(analyze_fault_codes_with_gpt("P0171, P0301"))

    # Simulate processing of a command
    class MockCarControls:
        def window_control(self, window, action):
            return {"status": "success", "message": f"{action} {window} window."}

        def ac_control(self, action, temperature=None):
            return {"status": "success", "message": f"{action} AC at {temperature if temperature else ''} degrees."}

        def media_control(self, action):
            return {"status": "success", "message": f"Media {action}."}

        def light_control(self, light_type, action):
            return {"status": "success", "message": f"{light_type} lights {action}."}

    # Instantiate mock controls for testing
    mock_controls = MockCarControls()
    print(gpt_process_command("Roll down all windows", mock_controls))
    print(gpt_process_command("Set air conditioning to 22 degrees", mock_controls))
    print(gpt_process_command("Play media", mock_controls))
    print(gpt_process_command("Turn on headlights", mock_controls))
