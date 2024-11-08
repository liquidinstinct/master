
class DieselMileage:
    def __init__(self, sensor_backend):
        """
        Initializes the DieselMileage module with a backend interface for sensor control.
        
        Args:
            sensor_backend (object): An instance of the backend responsible for sensor control.
        """
        self.total_distance = 0
        self.total_fuel_consumed = 0
        self.sensor_backend = sensor_backend  # Backend for controlling sensors
        self.sensors = {
            "fuel_sensor": False,
            "distance_sensor": False,
            "temperature_sensor": False
        }

    def add_trip(self, distance_km, fuel_liters):
        """
        Adds a new trip data.
        
        Args:
            distance_km (float): Distance traveled in kilometers.
            fuel_liters (float): Fuel consumed in liters.
        """
        self.total_distance += distance_km
        self.total_fuel_consumed += fuel_liters

    def get_mileage(self):
        """
        Calculates the diesel mileage.

        Returns:
            float: Mileage in kilometers per liter (km/L).
        """
        if self.total_fuel_consumed == 0:
            return 0
        return self.total_distance / self.total_fuel_consumed

    def reset_data(self):
        """
        Resets the total distance and fuel data.
        """
        self.total_distance = 0
        self.total_fuel_consumed = 0

    def toggle_sensor(self, sensor_name, state):
        """
        Turns a sensor on or off.

        Args:
            sensor_name (str): Name of the sensor to toggle.
            state (bool): True to turn on, False to turn off.
        """
        if sensor_name in self.sensors:
            self.sensors[sensor_name] = state
            self.sensor_backend.control_sensor(sensor_name, state)
        else:
            raise ValueError(f"Sensor {sensor_name} not found.")
