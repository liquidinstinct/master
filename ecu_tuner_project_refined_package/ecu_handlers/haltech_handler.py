import serial
from serial.tools import list_ports
import logging

class HaltechHandler:
    def __init__(self, connection):
        self.connection = connection
        logging.info("HaltechHandler initialized with Haltech ECU connection.")

    # Placeholder for other HaltechHandler methods like read_data, decode_haltech_response, etc.

def auto_detect_haltech_com():
    """
    Detects available CP2102 COM ports (USB to UART Bridge) and attempts to connect to a Haltech ECU
    with various baud rates. Returns a serial connection if successful, otherwise None.
    """
    # Define typical baud rates for Haltech ECUs
    baud_rates = [115200, 57600, 38400, 19200, 9600]
    available_ports = list_ports.comports()

    # Log all available ports for debugging
    logging.info("Starting Haltech ECU detection. Available ports:")
    for port in available_ports:
        logging.info(f"Port: {port.device} - Description: {port.description}")

    # Attempt connection on ports with "CP2102" or "USB to UART Bridge" in their description
    for port in available_ports:
        if "CP2102" in port.description or "USB to UART" in port.description:
            for baud_rate in baud_rates:
                try:
                    logging.info(f"Attempting connection on {port.device} with baud rate {baud_rate}")
                    connection = serial.Serial(port.device, baudrate=baud_rate, timeout=3)

                    # Send a Haltech-specific initialization command (update this command as needed)
                    init_command = b'HALTECH_INIT_COMMAND\r'
                    connection.write(init_command)
                    
                    # Read response and log for validation
                    response = connection.read(64).strip()
                    logging.info(f"Response received from {port.device}: {response}")

                    # Check if response is valid (replace with actual expected response check if known)
                    if response:
                        logging.info(f"Connected to Haltech ECU on {port.device} at baud rate {baud_rate}")
                        return connection
                    
                    # Close the connection if no valid response
                    connection.close()
                    logging.info(f"No valid response from {port.device} at baud rate {baud_rate}. Connection closed.")

                except serial.SerialException as e:
                    logging.warning(f"Failed to connect on {port.device} at baud rate {baud_rate}: {e}")

    # If no connection is found, log and return None
    logging.warning("No Haltech COM port connection found after scanning all ports and baud rates.")
    return None
