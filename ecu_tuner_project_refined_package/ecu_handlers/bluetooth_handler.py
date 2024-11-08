import serial
import logging
import asyncio

class BluetoothHandler:
    def __init__(self, incoming_port="COM3", outgoing_port="COM5", baudrate=9600):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.baudrate = baudrate
        self.incoming_connection = None
        self.outgoing_connection = None

    def connect(self):
        """
        Establishes a Serial Bluetooth connection using specified COM ports.
        """
        try:
            # Open incoming and outgoing serial connections
            self.incoming_connection = serial.Serial(self.incoming_port, self.baudrate, timeout=1)
            self.outgoing_connection = serial.Serial(self.outgoing_port, self.baudrate, timeout=1)
            logging.info(f"Connected on incoming port {self.incoming_port} and outgoing port {self.outgoing_port}")
        except Exception as e:
            logging.error(f"Failed to connect on COM ports: {e}")
            raise ConnectionError(f"Bluetooth connection failed: {e}")

    def disconnect(self):
        """
        Closes the Serial Bluetooth connections.
        """
        if self.incoming_connection and self.incoming_connection.is_open:
            self.incoming_connection.close()
            logging.info(f"Disconnected from incoming port {self.incoming_port}")
        if self.outgoing_connection and self.outgoing_connection.is_open:
            self.outgoing_connection.close()
            logging.info(f"Disconnected from outgoing port {self.outgoing_port}")

    def send_data(self, data):
        """
        Sends data to the outgoing COM port.
        """
        if not self.outgoing_connection or not self.outgoing_connection.is_open:
            raise ConnectionError("Outgoing Bluetooth connection is not established.")
        
        try:
            self.outgoing_connection.write(data.encode())
            logging.info(f"Sent data: {data}")
        except Exception as e:
            logging.error(f"Error sending data: {e}")
            raise IOError(f"Failed to send data over Bluetooth: {e}")

    def receive_data(self):
        """
        Receives data from the incoming COM port.
        """
        if not self.incoming_connection or not self.incoming_connection.is_open:
            raise ConnectionError("Incoming Bluetooth connection is not established.")
        
        try:
            data = self.incoming_connection.readline().decode().strip()
            logging.info(f"Received data: {data}")
            return data
        except Exception as e:
            logging.error(f"Error receiving data: {e}")
            raise IOError(f"Failed to receive data over Bluetooth: {e}")

    def is_connected(self):
        """
        Checks if both incoming and outgoing COM connections are active.
        """
        return (self.incoming_connection and self.incoming_connection.is_open and
                self.outgoing_connection and self.outgoing_connection.is_open)
