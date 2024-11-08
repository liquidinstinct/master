# Python code for app.py

import serial
import logging
import asyncio
from flask import Flask, jsonify, request, render_template
from ecu_handlers.obd2_handler import OBD2Handler, auto_detect_ecu, auto_detect_bluetooth_obd
from ecu_handlers.haltech_handler import HaltechHandler, auto_detect_haltech_com
from ecu_handlers.gpt_handler import analyze_fault_codes_with_gpt
from ecu_handlers.bluetooth_handler import BluetoothHandler
import pyttsx3
import os

app = Flask(__name__)

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Global variables for handler and connection details
handler_type = None
ecu_connection = None
obd_handler = None
bluetooth_handler = BluetoothHandler(incoming_port="COM3", outgoing_port="COM5", baudrate=9600)

# TTS function for voice feedback
def speak(message):
    tts_engine.say(message)
    tts_engine.runAndWait()

# Root route to render the HTML dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Function to auto-detect and initialize the ECU type with OBD-II priority
def initialize_handler():
    global obd_handler, ecu_connection, handler_type
    logging.info("Attempting to auto-detect ECU type...")

    # Attempt OBD-II detection first
    ecu_connection = auto_detect_bluetooth_obd() or auto_detect_ecu()
    if ecu_connection:
        handler_type = "obd2"
        obd_handler = OBD2Handler(ecu_connection)
        logging.info("OBD-II ECU detected and initialized.")
        speak("OBD-II ECU detected and initialized.")
        return

    # If OBD-II detection fails, attempt Haltech detection
    ecu_connection = auto_detect_haltech_com()
    if ecu_connection:
        handler_type = "haltech"
        obd_handler = HaltechHandler(ecu_connection)
        logging.info("Haltech ECU detected and initialized.")
        speak("Haltech ECU detected and initialized.")
        return

    # If no compatible ECU is detected
    handler_type = None
    obd_handler = None
    logging.error("Failed to detect any compatible ECU.")
    speak("Failed to detect any compatible ECU.")

# Call the auto-detection function on startup
initialize_handler()

# --- ECU Control and Status Endpoints ---
@app.route('/api/tune/set_handler', methods=['POST'])
def set_handler():
    global handler_type, obd_handler
    data = request.get_json()
    selected_handler = data.get("handler", "").lower()

    if selected_handler not in ["obd2", "haltech"]:
        return jsonify({"status": "error", "message": "Invalid handler type"}), 400

    handler_type = selected_handler
    initialize_handler()
    speak(f"{handler_type.capitalize()} handler selected")
    return jsonify({"status": "success", "message": f"{handler_type.capitalize()} handler selected"})

@app.route('/api/tune/connection_status', methods=['GET'])
def connection_status():
    connected = obd_handler is not None and hasattr(obd_handler, 'serial_connection') and obd_handler.serial_connection.is_open
    return jsonify({"connected": connected})

@app.route('/api/tune/read_data', methods=['GET'])
def read_data():
    parameter = request.args.get("parameter")
    if not obd_handler or not parameter:
        return jsonify({"status": "error", "message": "ECU connection or parameter missing"}), 400

    try:
        data = obd_handler.read_data(parameter)
        speak(f"{parameter} data is {data}")
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logging.error(f"Error reading data for {parameter}: {e}")
        return jsonify({"status": "error", "message": f"Error reading {parameter} data"}), 500

# --- Fault Code and GPT Analysis ---
@app.route('/api/tune/read_fault_codes', methods=['GET'])
def read_fault_codes():
    if not obd_handler:
        return jsonify({"status": "error", "message": "No ECU connection detected"}), 500

    try:
        fault_codes = obd_handler.read_fault_codes()
        message = "No faults detected" if not fault_codes else f"Fault codes: {', '.join(fault_codes)}"
        speak(message)
        return jsonify({"status": "success", "codes": fault_codes})
    except Exception as e:
        logging.error(f"Error reading fault codes: {e}")
        return jsonify({"status": "error", "message": "Error reading fault codes"}), 500

# Placeholder for async function
async def my_async_function():
    # async code here
    pass

