import logging
from obd2_handler import OBD2Handler, auto_detect_ecu
from haltech_handler import HaltechHandler
from gpt_handler import GPTHandler

class TuningHandler:
    def __init__(self):
        logging.info("Initializing TuningHandler")
        self.gpt_handler = GPTHandler()  # Initialize GPTHandler
        self.ecu_handler = None
        self.select_ecu_handler()

    def select_ecu_handler(self):
        self.ecu_connection = auto_detect_ecu()
        if self.ecu_connection:
            self.ecu_handler = OBD2Handler(self.ecu_connection)
            logging.info("Using OBD2Handler.")
        else:
            self.ecu_handler = HaltechHandler()
            logging.info("Using HaltechHandler in fallback mode.")

    def read_engine_data(self):
        if self.ecu_handler:
            return {
                "rpm": self.ecu_handler.read_data("rpm"),
                "speed": self.ecu_handler.read_data("speed"),
                "afr": self.ecu_handler.read_data("afr"),
            }
        return {}

    def suggest_tuning_modifications(self):
        engine_data = self.read_engine_data()
        return self.gpt_handler.suggest_tuning_modifications(engine_data)
