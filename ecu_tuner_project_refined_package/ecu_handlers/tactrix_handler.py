from tactrix_handler import TactrixHandler

tactrix = TactrixHandler()
rpm_data = tactrix.read_data('010C')  # Example command to read RPM
if rpm_data:
    print(f"RPM data: {rpm_data}")
tactrix.disconnect()

