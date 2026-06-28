# SMART CITY TRANSPORT SYSTEM - UGANDA VERSION

# Base Class
class Vehicle:
    def __init__(self, registration_number, manufacturer, speed):
        self.registration_number = registration_number
        self.manufacturer = manufacturer
        self.speed = speed
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            print(f"{self.registration_number} started.")
        else:
            print(f"{self.registration_number} is already running.")

    def stop(self):
        if self.is_running:
            self.is_running = False
            print(f"{self.registration_number} stopped.")
        else:
            print(f"{self.registration_number} is already stopped.")

    def display_info(self):
        return (
            f"Registration Number: {self.registration_number}, "
            f"Manufacturer: {self.manufacturer}, "
            f"Speed: {self.speed} km/h"
        )


# Public Bus Class
class PublicBus(Vehicle):
    def __init__(self, registration_number, manufacturer, speed,
                 route_number, passenger_capacity):

        Vehicle.__init__(self, registration_number, manufacturer, speed)

        self.route_number = route_number
        self.passenger_capacity = passenger_capacity

    def announce_route(self):
        print(
            f"Bus {self.registration_number} is travelling on "
            f"the {self.route_number} route."
        )

    def display_info(self):
        return (
            f"{Vehicle.display_info(self)}, "
            f"Route: {self.route_number}, "
            f"Passenger Capacity: {self.passenger_capacity}"
        )


# Electric Vehicle Class
class ElectricVehicle(Vehicle):
    def __init__(self, registration_number, manufacturer, speed,
                 battery_percentage):

        Vehicle.__init__(self, registration_number, manufacturer, speed)

        self.battery_percentage = battery_percentage
        self.charging_status = False

    def charge(self):
        if self.battery_percentage < 100:
            self.charging_status = True
            print(f"{self.registration_number} is charging...")

            # Simulate charging
            self.battery_percentage = 100

            self.charging_status = False
            print(f"{self.registration_number} fully charged.")
        else:
            print(f"{self.registration_number} battery already full.")

    def display_info(self):
        return (
            f"{Vehicle.display_info(self)}, "
            f"Battery: {self.battery_percentage}%"
        )


# Electric Bus Class (Multiple Inheritance)
class ElectricBus(PublicBus, ElectricVehicle):
    def __init__(self, registration_number, manufacturer, speed,
                 route_number, passenger_capacity, battery_percentage):

        PublicBus.__init__(
            self,
            registration_number,
            manufacturer,
            speed,
            route_number,
            passenger_capacity
        )

        self.battery_percentage = battery_percentage
        self.charging_status = False

    def display_info(self):
        return (
            f"Registration Number: {self.registration_number}, "
            f"Manufacturer: {self.manufacturer}, "
            f"Speed: {self.speed} km/h, "
            f"Route: {self.route_number}, "
            f"Passenger Capacity: {self.passenger_capacity}, "
            f"Battery: {self.battery_percentage}%"
        )


# Main Program
def main():

    print("=" * 60)
    print("SMART CITY TRANSPORT SYSTEM - UGANDA")
    print("=" * 60)

    # Create Objects
    car = Vehicle(
        "UBA 123A",
        "Toyota Uganda",
        120
    )

    bus = PublicBus(
        "UBB 456B",
        "Kiira Motors",
        80,
        "Kampala - Mukono",
        45
    )

    ev = ElectricVehicle(
        "UBE 789C",
        "Kiira EV",
        140,
        75
    )

    ebus = ElectricBus(
        "UBF 321D",
        "Kiira Motors",
        70,
        "Kampala - Entebbe",
        50,
        60
    )

    # Vehicle Information
    print("\n1. VEHICLE INFORMATION")
    print("-" * 60)

    print(car.display_info())
    print(bus.display_info())
    print(ev.display_info())
    print(ebus.display_info())

    # Starting Vehicles
    print("\n2. STARTING VEHICLES")
    print("-" * 60)

    car.start()
    bus.start()
    ev.start()
    ebus.start()

    # Stopping Vehicles
    print("\n3. STOPPING VEHICLES")
    print("-" * 60)

    car.stop()
    bus.stop()
    ev.stop()
    ebus.stop()

    # Charging Electric Vehicles
    print("\n4. CHARGING ELECTRIC VEHICLES")
    print("-" * 60)

    print(f"Battery Before Charging: {ev.battery_percentage}%")
    ev.charge()
    print(f"Battery After Charging: {ev.battery_percentage}%")

    print()

    print(f"Electric Bus Battery Before Charging: {ebus.battery_percentage}%")
    ebus.charge()
    print(f"Electric Bus Battery After Charging: {ebus.battery_percentage}%")

    # Route Announcements
    print("\n5. BUS ROUTE ANNOUNCEMENTS")
    print("-" * 60)

    bus.announce_route()
    ebus.announce_route()

    # Inheritance Demonstration
    print("\n6. INHERITANCE CHECK")
    print("-" * 60)

    print("Is ElectricBus a Vehicle?",
          isinstance(ebus, Vehicle))

    print("Is ElectricBus a PublicBus?",
          isinstance(ebus, PublicBus))

    print("Is ElectricBus an ElectricVehicle?",
          isinstance(ebus, ElectricVehicle))

    # Demonstrating Inherited Methods
    print("\n7. INHERITED METHOD ACCESS")
    print("-" * 60)

    print("Using start() inherited from Vehicle:")
    ebus.start()

    print("\nUsing announce_route() inherited from PublicBus:")
    ebus.announce_route()

    print("\nUsing charge() inherited from ElectricVehicle:")
    ebus.charge()

    # Method Resolution Order
    print("\n8. METHOD RESOLUTION ORDER (MRO)")
    print("-" * 60)

    for cls in ElectricBus.__mro__:
        print(cls.__name__)

    # Inheritance Hierarchy Summary
    print("\n9. INHERITANCE HIERARCHY")
    print("-" * 60)

    print("=" * 60)
    print("PROGRAM EXECUTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()