# restaurantsystem.py
# Restaurant Automation System
# Version 1.4.5
# Created by Melih Can Demir

# Importing necessary libraries
from pyfiglet import figlet_format as figlet
from colorama import Fore as color
from tabulate import tabulate
from datetime import datetime
import uuid
import logging_utils

logging_utils.setup_logging()

def generate_order_id():
    return str(uuid.uuid4().hex)[:8]  # Generate an 8-character alphanumeric ID

# Restaurant Order and Payment Automation
class RestaurantOrderSystem():
    def __init__(self, database_manager):
        # Initialize menu dictionary and database connection variables
        self.menu = {}
        self.menu_data = []
        self.database_manager = database_manager
        self.name = str()
        self.customer_balance = int()
        self.customer_tip = int()
        self.order_price = int()

    def setup_database(self, sort_by_price=False):
        try:
            # Connect to the database and fetch menu data
            self.database_manager.connect()

            # Fetch menu data with optional sorting by price
            if sort_by_price:
                self.menu_data = self.database_manager.fetch_all("SELECT name, price FROM menu ORDER BY price") 
            
            else:
                self.menu_data = self.database_manager.fetch_all("SELECT name, price FROM menu")

            # Populate menu dictionary with menu items and prices
            for name, price in self.menu_data:
                self.menu[name] = price

        except Exception as e:
            print("An error occurred:", e)
            # Log the error
            logging_utils.log_error(f"An error occurred: {e}")

    def customer_menu(self):
        self.selected_items = []  # Initialize an empty list for selected menu items

        try:
            while True:
                self.menu_choice = input("\nPlease enter the number of the menu item you want to order (0 to finish ordering): ")

                if self.menu_choice.lower() == '0':
                    break

                if self.menu_choice.isdigit():
                    self.menu_choice = int(self.menu_choice)
                    if 1 <= self.menu_choice <= len(self.menu_data):
                        self.selected_menu_item = self.menu_data[self.menu_choice - 1][0]
                        # Ask for the quantity
                        while True:
                            quantity = input(f"How many {self.selected_menu_item} would you like to order: ")
                            if quantity.isdigit():
                                quantity = int(quantity)
                                if quantity >= 1:
                                    break
                                else:
                                    print("Quantity must be at least 1.")
                            else:
                                print("Invalid input. Please enter a valid quantity (a positive integer).")
                        
                        # Check if the item is already in selected_items
                        existing_item = next((item for item in self.selected_items if item[0] == self.selected_menu_item), None)
                        if existing_item:
                            # If the item already exists, increment its quantity
                            index = self.selected_items.index(existing_item)
                            self.selected_items[index] = (self.selected_menu_item, existing_item[1] + quantity)
                        
                        else:
                            # If it's a new item, add it to selected_items with quantity 1
                            self.selected_items.append((self.selected_menu_item, quantity))
                        
                        print("=" * 50)
                        print(f"You selected: {self.selected_menu_item} - ${self.menu[self.selected_menu_item]}")
                        print("=" * 50)
                        print(f"Thanks for your order, {self.name}!")
                        print("Your order will be ready in ~10 minutes.")
                        print("=" * 50)
                    else:
                        print("Invalid menu number. Please choose a valid number.")
                else:
                    print("Invalid input. Please enter a number.")

        except KeyboardInterrupt as e:
            print("\n")
            print("*" * 50)
            print("Exiting the Program...")
            print("*" * 50)
            logging_utils.log_info(f"An error occurred: Keyboard Interrupt Ctrl+C")
            exit()
        
    def calculate_total_price(self, selected_items):
        total_price = sum(self.menu[item] for item in selected_items)
        return total_price

    def display_menu(self):
        try:
            print("     -- Here is the Menu List --     ")
            # Display the menu items and prices
            menu_table = []
            for index, (name, price) in enumerate(self.menu_data, start=1):
                menu_table.append([index, name, "${:.2f}".format(float(price))])
        
            table_headers = ["#", "Menu Item", "Price"]
            menu_table_str = tabulate(menu_table, headers=table_headers, tablefmt="grid")
            print(menu_table_str)

        except Exception as e:
            print("An error occurred:", e)
            logging_utils.log_error(f"An error occurred: {e}")

    def salutation_customer(self):
        # Welcome and ask for the customer's name
        print("Welcome Restaurant!\n")
        print(color.LIGHTBLUE_EX)
        ascii_art = figlet("Hello",font='roman')
        print(ascii_art)
        print("What are you eating or drinking today ?\n")
        self.name = input("Hello there! What is your name?\n\n")

    def payment_process(self):
        while True:
            try:
                # Get payment method and validate it
                self.payment_method = input("Cash or Creditcard:").capitalize()
                if self.payment_method == "Creditcard" or self.payment_method == "Cash":
                    self.customer_balance = float(input("\nEnter the amount to pay $"))
                    prices = float(self.menu[self.selected_menu_item])
                    if self.customer_balance >= prices:
                        print("Payment Confirmed.")
                        break
                    else:
                        print("Insufficient Balance!")
                        print("Please Try Again or Change Payment Method!")
                else:
                    print("Invalid Payment Method!")

            except ValueError:
                print("\n")
                print("*"*50)
                print("Please enter a numeric value")
                logging_utils.log_info(f"An error occurred: Enter numeric value")
                print("*"*50)

            except KeyboardInterrupt:
                print("\n")
                print("*"*50)
                print("Exiting the Program...")
                print("*"*50)
                logging_utils.log_info(f"An error occurred: Keyboard Interrupt Ctrl+C")
                exit()

    def waitress_tip(self):
        while True:
            try:
                # Get tip amount and validate it
                self.customer_tip = float(input("Would you like to tip $"))
                print("-"*50)

                if self.customer_balance >= float(self.order_price) + self.customer_tip and self.customer_tip >= 0:
                    print(f"{self.name} Thanks for the tips.")
                    print(f"Tip: ${self.customer_tip:.2f}")
                    print("Thank you for choosing us.")
                    print("Have a nice day!")
                    self.invoice(self.selected_items)
                    break

                else:
                    print("Balance is not enough to pay the tip.")
                    print(f"Tip is invalid: ${self.customer_tip:.2f}")
                print("-"*50)

            except ValueError:
                print("Please enter a numeric value")
                logging_utils.log_info(f"An error occurred: Enter a $ value for waitress tip!")
            

    def invoice(self, selected_items):
        try:
            # Calculate the change, taxes, and total price
            self.taxes = sum(float(self.menu[item[0]]) * 8 / 100 * item[1] for item in selected_items)
            self.total_price = sum(float(self.menu[item[0]]) * item[1] for item in selected_items)
            self.change = float(self.customer_balance) - self.total_price - float(self.customer_tip) - self.taxes
            self.total = self.total_price + float(self.customer_tip) + self.taxes
            self.order_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # print(f"Selected items: {selected_items}")  # Add this line for debugging

            # Check if the change is greater than or equal to zero
            if self.change >= 0:
                # Initialize a dictionary to store item quantities
                item_quantities = {}

                # Iterate through selected_items and accumulate quantities for the same item
                for item, quantity in selected_items:
                    if item in item_quantities:
                        item_quantities[item] += quantity
                    else:
                        item_quantities[item] = quantity

                # Create the invoice items list with quantities
                invoice_items = []
                for item, quantity in item_quantities.items():
                    item_price = float(self.menu[item])
                    description = f"{item} x{quantity}"  # Format item with quantity
                    amount = "${:.2f}".format(item_price * quantity)
                    invoice_items.append({"Description": description, "Amount": amount})
                # Create a list of dictionaries to represent invoice details
                invoice_data = [
                    {"Description": "Restaurant Invoice", "Amount": ""},
                    {"Description": "", "Amount": ""},  # Empty row for spacing
                    {"Description": "Order ID", "Amount": generate_order_id()},  # Generate a unique order ID
                    {"Description": "Order Date and Time", "Amount": self.order_date_time},
                    {"Description": "", "Amount": ""},
                    {"Description": "Name", "Amount": self.name},  # Customer name
                ]

                # Add selected items and their prices to the invoice
                for item in invoice_items:
                    invoice_data.append({"Description": item["Description"], "Amount": item["Amount"]})

                # Add the rest of the invoice details (tip, taxes, total, payment, change, note)
                invoice_data.extend([
                    {"Description": "Tip", "Amount": "${:.2f}".format(float(self.customer_tip))},
                    {"Description": "Tax", "Amount": "${:.2f}".format(float(self.taxes))},
                    {"Description": "Total", "Amount": "${:.2f}".format(self.total)},
                    {"Description": "Payment", "Amount": "${:.2f}".format(float(self.customer_balance))},
                    {"Description": "Change", "Amount": "${:.2f}".format(self.change)},
                    {"Description": "", "Amount": ""},
                    {"Description": "Note", "Amount": "Thank you for choosing us."},
                ])

                # Create the invoice table as a string
                invoice_table = tabulate(invoice_data, tablefmt="grid")

                # Print the invoice table
                print(invoice_table)

                # Save the invoice table to a file (optional)
                with open("data/invoice.txt", "w") as file:
                    file.write(invoice_table)
            
            else:
                print("Insufficient payment for the order")
        
        except Exception as e:
            print(f"An error occurred: {e}")