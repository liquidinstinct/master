import binascii
import logging

class ECUDataEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_binary()

    def load_binary(self):
        try:
            with open(self.file_path, 'rb') as f:
                self.binary_data = bytearray(f.read())
            logging.info(f"Binary data loaded from {self.file_path}")
        except FileNotFoundError:
            logging.error("File not found. Ensure the file exists and try again.")
            self.binary_data = None

    def read_value(self, offset, length):
        """Read a hex value from specified offset and length."""
        if not self.binary_data:
            return None
        value = self.binary_data[offset:offset + length]
        return binascii.hexlify(value).decode()

    def write_value(self, offset, hex_value):
        """Write a hex value at specified offset."""
        if not self.binary_data:
            return None
        value_bytes = binascii.unhexlify(hex_value)
        self.binary_data[offset:offset + len(value_bytes)] = value_bytes
        logging.info(f"Written hex value {hex_value} at offset {offset}")

    def save_binary(self, new_file_path):
        """Save modified binary to a new file."""
        if not self.binary_data:
            return None
        with open(new_file_path, 'wb') as f:
            f.write(self.binary_data)
        logging.info(f"Modified binary saved to {new_file_path}")
