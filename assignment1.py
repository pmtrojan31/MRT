class Vehicle():
    vehicle_type = 'Car'

    def __init__(self, vehicle_id, make, model, year, rental_rate, availability: bool, current_customer=None, reservations=None):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.rental_rate = rental_rate
        self.availability = availability
        self.current_customer = current_customer if current_customer else None
        self.reservations = reservations if reservations else []

    def display_vehicle_details(self):
        print(f"ID: {self.vehicle_id}, Make: {self.make}, Year: {self.year}, Rate: {self.rental_rate}, Available: {self.availability}")
    
    def rent_vehicle(self, customer):
        if self.availability and not customer.current_vehicle:
            print(f"Congratulations, you have rented {self.make} {self.model}")
            self.availability = False
            self.current_customer = customer
            customer.current_vehicle = self
            customer.rental_history.append(self)
        else:
            print("Vehicle is unavailable.")

    def return_vehicle(self):
        print(f"Vehicle {self.make} {self.model} returned.")
        self.availability = True
        self.current_customer.current_vehicle = None
        self.current_customer = None
    
    def reserve_vehicle(self, customer):
        if not customer.current_reservation:
            print(f"Vehicle {self.make} {self.model} reserved by {customer.name}.")
            self.reservations.append(customer)
            self.availability = False
            customer.current_reservation = self
        else:
            print("Only one vehicle can be reserved at a time.")

class LuxuryVehicle(Vehicle):
    def __init__(self, vehicle_id, make, model, year, rental_rate, availability, extra_features):
        super().__init__(vehicle_id, make, model, year, rental_rate * 1.2, availability)
        self.extra_features = extra_features
    
    def display_extra_features(self):
        print(f"Luxury Features: {self.extra_features}")

class Customer():
    def __init__(self, customer_id, name, contact_info, rental_history : list=None, current_vehicle=None, current_reservation : Vehicle=None):
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info
        self.rental_history = rental_history if rental_history else []
        self.current_vehicle = current_vehicle
        self.current_reservation = current_reservation

    def display_customer_details(self):
        print(f"ID: {self.customer_id}, Name: {self.name}, Contact: {self.contact_info}")

    def display_rental_history(self):
        print("Rental History:")
        for rental in self.rental_history:
            print(f"{rental.make} {rental.model} ({rental.year})")

class RegularCustomer(Customer):
    def __init__(self, customer_id, name, contact_info, rental_history, current_vehicle, loyalty_points=0):
        super().__init__(customer_id, name, contact_info, rental_history, current_vehicle)
        self.loyalty_points = loyalty_points
    
    def earn_points(self, points):
        self.loyalty_points += points
        print(f"{self.name} earned {points} loyalty points.")

class PremiumCustomer(Customer):
    def __init__(self, customer_id, name, contact_info, rental_history, current_vehicle=None):
        super().__init__(customer_id, name, contact_info, rental_history, current_vehicle)
    
    def apply_for_discount(self, rental_rate):
        return rental_rate * 0.9

class RentalManager():
    def __init__(self, all_vehicles):
        self.all_vehicles = all_vehicles
        self.available_vehicles = [vehicle for vehicle in self.all_vehicles if vehicle.availability]

    def add_vehicle(self, vehicle):
        self.all_vehicles.append(vehicle)
        if vehicle.availability:
            self.available_vehicles.append(vehicle)
    
    def remove_vehicle(self, vehicle):
        self.all_vehicles.remove(vehicle)
        if vehicle in self.available_vehicles:
            self.available_vehicles.remove(vehicle)
    
    def generate_report(self):
        print("Vehicle Report:")
        for vehicle in self.all_vehicles:
            vehicle.display_vehicle_details()
            if vehicle.current_customer:
                print(f"Current Customer: {vehicle.current_customer.name}")
            if vehicle.reservations:
                if vehicle.reservations[-1].current_reservation:
                    print(f"Currently reserved: {vehicle.reservations[-1].name}")
    
    def display_vehicles_for_customer(self):
        print("Available Vehicles:")
        for vehicle in self.available_vehicles:
            vehicle.display_vehicle_details()

    def update_availability(self):
        self.available_vehicles = [vehicle for vehicle in self.all_vehicles if vehicle.availability]

# Main Function to interact with the rental system
def main():
    vehicles = [
        Vehicle(1, "Toyota", "Camry", 2020, 45.99, True),
        Vehicle(2, "Honda", "Civic", 2019, 40.50, True),
        Vehicle(3, "Ford", "Mustang", 2021, 75.00, True),
        Vehicle(4, "Chevrolet", "Impala", 2018, 38.25, True),
        Vehicle(5, "BMW", "X5", 2022, 85.99, True),
        Vehicle(6, "Tesla", "Model 3", 2023, 99.99, True),
        Vehicle(7, "Nissan", "Altima", 2020, 42.00, True),
        Vehicle(8, "Jeep", "Wrangler", 2021, 60.75, True),
        Vehicle(9, "Audi", "A4", 2019, 70.25, True),
        Vehicle(10, "Mercedes", "C-Class", 2022, 95.50, True)
    ]

    manager = RentalManager(vehicles)

    while True:
        customer_input = eval(input("Enter customer details as a list: ['Customer Type', 'ID', 'Name', 'Contact', 'Rental History'].\n"))
        if type(customer_input) == list:
            if customer_input[0] == "Regular Customer":
                our_customer = RegularCustomer(customer_input[1], customer_input[2], customer_input[3], customer_input[4], None, 0)
            else:
                our_customer = PremiumCustomer(customer_input[1], customer_input[2], customer_input[3], customer_input[4])
        else:
            break

        while True:
            choice = int(input("1. Rent a vehicle\n2. Return a vehicle\n3. View customer details\n4. View rental history\n5. Add new vehicle\n6. Remove vehicle\n7. Generate vehicle report\n8. View available vehicles\n9. Make reservations\n10. Exit\n"))
            if choice == 1:
                manager.display_vehicles_for_customer()
                vehicle_choice_id = int(input("Enter the vehicle ID you want to rent: "))
                selected_vehicle = next((vehicle for vehicle in manager.all_vehicles if vehicle.vehicle_id == vehicle_choice_id), None)
                if selected_vehicle:
                    selected_vehicle.rent_vehicle(our_customer)
                    manager.update_availability()
                else:
                    print("Invalid vehicle ID.")
            elif choice == 2:
                if our_customer.current_vehicle:
                    our_customer.current_vehicle.return_vehicle()
                    manager.update_availability()
                else:
                    print("You have no vehicle to return.")
            elif choice == 3:
                our_customer.display_customer_details()
            elif choice == 4:
                our_customer.display_rental_history()
            elif choice == 5:
                vehicle_details = eval(input("Enter vehicle details: [ID, Make, Model, Year, Rate, Availability]\n"))
                new_vehicle = Vehicle(vehicle_details[0], vehicle_details[1], vehicle_details[2], vehicle_details[3], vehicle_details[4], vehicle_details[5])
                manager.add_vehicle(new_vehicle)
            elif choice == 6:
                vehicle_id = int(input("Enter the vehicle ID to remove: "))
                vehicle_to_remove = next((vehicle for vehicle in manager.all_vehicles if vehicle.vehicle_id == vehicle_id), None)
                if vehicle_to_remove:
                    manager.remove_vehicle(vehicle_to_remove)
                    manager.update_availability()
                else:
                    print("Invalid vehicle ID.")
            elif choice == 7:
                manager.generate_report()
            elif choice == 8:
                manager.display_vehicles_for_customer()
            elif choice == 9:
                vehicle_choice_id = int(input("Enter the vehicle ID to reserve: "))
                selected_vehicle = next((vehicle for vehicle in manager.all_vehicles if vehicle.vehicle_id == vehicle_choice_id), None)
                if selected_vehicle:
                    selected_vehicle.reserve_vehicle(our_customer)
                    manager.update_availability()
                else:
                    print("Invalid vehicle ID.")
            elif choice == 10:
                break

# Call the main function to start the program
if __name__ == "__main__":
    main()





    
        



    


