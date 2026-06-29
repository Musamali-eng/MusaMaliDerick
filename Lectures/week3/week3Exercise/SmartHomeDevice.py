# ==========================================
# SMART HOME DEVICES SYSTEM
# ==========================================

# Base Class
class SmartDevice:
    def __init__(self, device_name):
        self.device_name = device_name
        self.power_status = False

    def turn_on(self):
        self.power_status = True
        print(f"{self.device_name} is now ON.")

    def turn_off(self):
        self.power_status = False
        print(f"{self.device_name} is now OFF.")

    def device_info(self):
        status = "ON" if self.power_status else "OFF"
        print(f"Device: {self.device_name}")
        print(f"Status: {status}")


# Child Class 1
class SmartLight(SmartDevice):
    def __init__(self, device_name, brightness=50):
        super().__init__(device_name)
        self.brightness = brightness

    def adjust_brightness(self, level):
        self.brightness = level
        print(f"Brightness set to {self.brightness}%.")


# Child Class 2
class SmartThermostat(SmartDevice):
    def __init__(self, device_name, temperature=22):
        super().__init__(device_name)
        self.temperature = temperature

    def adjust_temperature(self, temp):
        self.temperature = temp
        print(f"Temperature set to {self.temperature}°C.")


# ==========================================
# MAIN PROGRAM
# ==========================================

# Create Smart Light
light = SmartLight("Living Room Light")

# Create Smart Thermostat
thermostat = SmartThermostat("Bedroom Thermostat")

print("===== SMART LIGHT =====")
light.turn_on()              # Inherited method
light.adjust_brightness(80)  # Device-specific method
light.device_info()

print("\n" + "=" * 40)

print("===== SMART THERMOSTAT =====")
thermostat.turn_on()               # Inherited method
thermostat.adjust_temperature(26)  # Device-specific method
thermostat.device_info()

print("\n" + "=" * 40)

# Turn devices off
light.turn_off()
thermostat.turn_off()