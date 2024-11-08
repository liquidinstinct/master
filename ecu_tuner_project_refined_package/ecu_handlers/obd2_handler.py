import logging
import serial
from serial.tools import list_ports

class OBD2Handler:
    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        logging.info("OBD2Handler initialized with ECU connection.")
        self.supports_write = False  # Set to False as OBD-II is typically read-only

    def read_data(self, parameter):
        """
        Reads data from the ECU for a specific parameter (e.g., RPM or Speed).
        """
        try:
            # OBD-II commands: "010C" for RPM, "010D" for Speed
            command = b'010C\r' if parameter == "rpm" else b'010D\r'
            self.serial_connection.write(command)
            response = self.serial_connection.read(64).strip()
            logging.info(f"Raw response for {parameter}: {response}")

            if response:
                decoded_response = self.decode_obd_response(response, parameter)
                logging.info(f"Decoded data for {parameter}: {decoded_response}")
                return decoded_response
            else:
                logging.warning(f"No response received for {parameter}")
                return None
        except Exception as e:
            logging.error(f"Failed to read data for {parameter}: {e}")
            return None

    def decode_obd_response(self, response, parameter):
        """
        Decodes the raw response from the ECU based on the OBD-II protocol.
        """
        try:
            # Convert bytes to hex string if needed
            hex_str = response.hex() if isinstance(response, bytes) else response
            if parameter == "rpm" and hex_str.startswith("410C"):
                rpm_value = int(hex_str[4:8], 16) / 4
                return f"{rpm_value:.0f} RPM"
            elif parameter == "speed" and hex_str.startswith("410D"):
                speed_value = int(hex_str[4:6], 16)
                return f"{speed_value} km/h"
            return hex_str
        except Exception as e:
            logging.error(f"Failed to decode OBD response for {parameter}: {e}")
            return response

def auto_detect_ecu():
    """
    Attempts to detect and connect to an ECU over USB COM port.
    Returns the serial connection object if successful, otherwise None.
    """
    available_ports = list_ports.comports()
    for port in available_ports:
        for baud in [9600, 115200]:  # Common baud rates for ECU
            try:
                logging.info(f"Attempting connection on {port.device} with baud rate {baud}")
                ser = serial.Serial(port.device, baudrate=baud, timeout=2)
                ser.write(b'0100\r')  # Send an OBD-II initialization command
                response = ser.read(64)
                if response:
                    logging.info(f"ECU detected on {port.device} with baud rate {baud}")
                    return ser
                ser.close()
            except serial.SerialException as e:
                logging.warning(f"Could not connect to port {port.device}: {e}")
                continue
    logging.warning("No ECU detected.")
    return None

def auto_detect_bluetooth_obd():
    """
    Detects Bluetooth OBD-II adapters by checking known COM ports associated with Bluetooth adapters.
    Returns the serial connection object if successful, otherwise None.
    """
    available_ports = list_ports.comports()
    for port in available_ports:
        if "Bluetooth" in port.description or "Standard Serial over Bluetooth" in port.description:
            try:
                logging.info(f"Attempting Bluetooth connection on {port.device}")
                ser = serial.Serial(port.device, baudrate=9600, timeout=2)  # Adjust baud rate if needed
                ser.write(b'0100\r')  # Send an OBD-II initialization command
                response = ser.read(64)
                if response:
                    logging.info(f"Bluetooth OBD-II adapter detected on {port.device}")
                    return ser
                ser.close()
            except serial.SerialException as e:
                logging.warning(f"Could not connect to Bluetooth OBD on {port.device}: {e}")
                continue
    logging.warning("No Bluetooth OBD-II adapter detected.")
    return None
