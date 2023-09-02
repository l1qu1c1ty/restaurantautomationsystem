# Restaurant Automation System
# Version 1.3.4
# Created by Melih Can Demir

# Importing necessary libraries
from pyfiglet import figlet_format as figlet
from colorama import Fore as color
from tabulate import tabulate
import random
import string

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(random.choice(characters) for _ in range(length))
    return random_password

# Restaurant Order and Payment Automation
class RestaurantOrderSystem():
    def __init__(self, database_manager):
        # Initialize menu dictionary and database connection variables
        self.menu = {}
        self.database_manager = database_manager
        self.name = str()

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

    def customer_menu(self):
        try:
            while True:
                self.menu_choice = input("\nPlease enter the number of the menu item you want to order: ")
                
                if self.menu_choice.isdigit():
                    self.menu_choice = int(self.menu_choice)
                    if 1 <= self.menu_choice <= len(self.menu_data):
                        self.selected_menu_item = self.menu_data[self.menu_choice - 1][0]
                        self.order_price = self.menu[self.selected_menu_item]
                        print("=" * 50)
                        print("You selected: {} - ${}".format(self.selected_menu_item, self.order_price))
                        print("=" * 50)
                        print("Thanks for your order, {}!".format(self.name))
                        print("Your order will be ready in ~10 minutes.")
                        print("=" * 50)
                        break
                    else:
                        print("Invalid menu number. Please choose a valid number.")
                else:
                    print("Invalid input. Please enter a number.")

        except KeyboardInterrupt:
            print("\n")
            print("*" * 50)
            print("Exiting the Program...")
            print("*" * 50)
            exit()

    def display_menu(self):
        try:
            # Display the menu items and prices
            menu_table = []
            for index, (name, price) in enumerate(self.menu_data, start=1):
                menu_table.append([index, name, "${:.2f}".format(float(price))])
        
            table_headers = ["#", "Menu Item", "Price"]
            menu_table_str = tabulate(menu_table, headers=table_headers, tablefmt="grid")
            print(menu_table_str)

        except Exception as e:
            print("An error occurred:", e)

    def salutation_customer(self):
        # Welcome and ask for the customer's name
        print("Welcome Restaurant!\n")
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
                print("*"*50)

            except KeyboardInterrupt:
                print("\n")
                print("*"*50)
                print("Exiting the Program...")
                print("*"*50)
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
                    break

                else:
                    print("Balance is not enough to pay the tip.")
                    print(f"Tip is invalid: ${self.customer_tip:.2f}")
                print("-"*50)

            except ValueError:
                print("Please enter a numeric value")

    def invoice(self):
        # Calculate the change
        self.change = self.customer_balance - float(self.order_price) - self.customer_tip
        
        # Check if the change is greater than or equal to zero
        if self.change >= 0:
            # Create a list of dictionaries to represent invoice details
            invoice_data = [
                {"Description": "Restaurant Invoice", "Amount": ""},
                {"Description": "", "Amount": ""},
                {"Description": "Menu Item", "Amount": "${:.2f}".format(float(self.order_price))},
                {"Description": "Payment", "Amount": "${:.2f}".format(float(self.customer_balance))},
                {"Description": "Tip", "Amount": "${:.2f}".format(float(self.customer_tip))},
                {"Description": "Change", "Amount": "${:.2f}".format(float(self.change))},
                {"Description": "Payment Method", "Amount": str(self.payment_method)},
            ]

            # Create the invoice table as a string
            invoice_table = tabulate(invoice_data, tablefmt="grid")

            # Print the invoice table
            print(invoice_table)

            # Save the invoice table to a file
            with open("../data/invoice.txt", "w") as file:
                file.write(invoice_table)
        else:
            print("Insufficient payment for the order")

        
    def discount_vouchers(self):
        discount = random.randint(1, 18)
        discounted_price = float(self.order_price) - (float(self.order_price) * discount / 100)
        # print(f"%{discount}")
        # print(discounted_price)

    def payment_refund(self):
        pass

class UserManager:
    def __init__(self, database_manager, restaurant_order_interface):
        self.database_manager = database_manager
        self.restaurant_order_interface = restaurant_order_interface

    def login_interface(self):
        max_attempts = 3
   
        while max_attempts > 0:
            try:
                # It allows the user to log in. If the user exists in the database, Its log in.
                # Otherwise, he continues in the guest session.
                self.database_manager.connect()
                self.username = input("Username: ")
                self.password = input("Password: ")
                self.database_manager.execute_query("SELECT username, password FROM login WHERE username = ?", (self.username,))
                row = self.database_manager.cursor.fetchone()
                if row:
                    db_username, db_password = row
                    if (self.username == db_username and self.password == db_password):
                        print("You have successfully logged in!") 
                        break
                    
                    else:
                        print("Incorrect username or password.")
                        max_attempts -= 1
                else:
                    print("User not found.")
                    max_attempts -= 1
            
            except Exception as e:
                print("An error occurred:", e)
        
        if max_attempts == 0:
            print("Too many incorrect attempts. Returning to the main menu.")
            self.restaurant_order_interface.start_option()
    
    def add_user(self):
        try:
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            login_data = (username, password)
            self.database_manager.execute_query("INSERT INTO login (username, password) VALUES (?, ?)", login_data)
            self.database_manager.commit()
            print("User added successfully!")
        
        except Exception as e:
            print("An error occurred while adding user:", e)
        

    def update_username(self):
        user_name = input("Enter the old user name: ")
        new_username = input("Enter the new user name: ")
        self.database_manager.execute_query("UPDATE login SET username = ? WHERE username = ?", (new_username, user_name))
        self.database_manager.commit()
        print("Username updated successfully!")
        
    def update_password(self):
        user_password = input("Enter the old password: ")
        new_password = input("Enter the new password: ")
        self.database_manager.execute_query("UPDATE login SET password = ? WHERE password = ?", (new_password, user_password))
        self.database_manager.commit()
        print("Password updated successfully!")
    
    def reset_password(self):
        try:
            username = input("Enter the username for which you want to reset the password: ")
            new_password = generate_random_password()  # Generate a random password

            self.database_manager.execute_query("UPDATE login SET password = ? WHERE username = ?", (new_password, username))
            self.database_manager.commit()
            
            print(f"The password for user '{username}' has been reset. The new password is: {new_password}")

        except Exception as e:
            print("An error occurred while resetting password:", e)

    def delete_account(self):
        self.database_manager.execute_query("DELETE FROM login WHERE username = ?",(self.username,))
        self.database_manager.commit()
    
    def log_out(self):
        pass

class Admin(UserManager):
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.restaurant = RestaurantOrderSystem(database_manager)

    def add_menu(self):
        menu_name = input("Enter menu name: ")
        menu_price = input("Enter menu price: ")
        menu_data = (menu_name,menu_price)
        self.database_manager.execute_query("INSERT INTO menu (name, price) VALUES (?, ?)", menu_data)
        self.database_manager.commit()
    
    def delete_menu(self):
        menu_name = input("Enter menu name: ")
        self.database_manager.execute_query("DELETE FROM menu WHERE name = ?",(menu_name,))
        self.database_manager.commit()
    
    def delete_user(self):
        username = input("Enter user name:")
        self.database_manager.execute_query("DELETE FROM login WHERE username = ?",(username,))
        self.database_manager.commit()

    def update_menu(self):
        try:
            menu_name = input("Enter the menu name to update: ")
            new_name = input("Enter the new name for the menu: ")
            self.database_manager.execute_query("UPDATE menu SET name = ? WHERE name = ?", (new_name, menu_name))
            self.database_manager.commit()
            print("Menu item updated successfully!")
        
        except Exception as e:
            print("An error occurred while updating menu:", e)

    def update_price(self):
        try:
            menu_name = input("Enter the menu name to update price: ")
            new_price = input("Enter the new price $")

            self.database_manager.execute_query("UPDATE menu SET price = ? WHERE name = ?", (new_price, menu_name))
            self.database_manager.commit()
            print("Menu price updated successfully!")
        
        except Exception as e:
            print("An error occurred:", e)
        

    def user_info(self):
        try:
            self.database_manager.execute_query("SELECT * FROM login")
            users = self.database_manager.fetch_all("SELECT * FROM login")
            headers = ["Username", "Password"]
            user_info_table = [[user[0], "*" * len(user[1])] for user in users]
            print(tabulate(user_info_table, headers=headers, tablefmt="fancy_grid"))
        
        except Exception as e:
            print("An error occurred while fetching user information:", e)
    
    def menu_info(self):
        self.restaurant.setup_database()
        self.restaurant.display_menu()
        

class RestaurantOrderInterface:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.restaurant = RestaurantOrderSystem(self.database_manager)
        self.usermanager = UserManager(self.database_manager, self)
        self.admin = Admin(self.database_manager)

    def get_option(self, options_dict):
        while True:
            option_input = input("\nEnter option number: ")
            if option_input.isdigit():
                option_number = int(option_input)
                selected_option = options_dict.get(option_number)
                if selected_option:
                    selected_option()
                    break
                else:
                    print("Error! Please enter a valid option number.")
            else:
                print("Error! Please enter a valid number.")

    def start_option(self):
        print(color.GREEN)
        print(figlet("Automation System",font="univers",width=120))
        print(color.LIGHTGREEN_EX)
        
        startup_options = [
            ("1", "Login"),
            ("2", "Sign in"),
            ("3", "Guest"),
            ("4", "Admin"),
            ("5", "User"),
            ("6", "Exit")
        ]

        headers = ["Option", "Description"]
        print(tabulate(startup_options, headers=headers, tablefmt="grid", colalign=("center", "left")))

        self.options = {
            1: self.usermanager.login_interface,
            2: self.usermanager.add_user,
            3: self.guest_option,
            4: self.admin_option,
            5: self.user_option,
            6: exit,
        }
        
        self.get_option(self.options)
            
    def admin_option(self):
        self.usermanager.login_interface()
        admin_options = [
            ("1", "Add User"),
            ("2", "Delete User"),
            ("3", "Add Menu"),
            ("4", "Delete Menu"),
            ("5", "Update Menu"),
            ("6", "Update Price"),
            ("7", "Show Users"),
            ("8", "Show Menu"),
            ("9","Reset Password"),
            ("10", "Log out"),
            ("11","Exit"),
            ("12","Back"),
            
        ]

        headers = ["Option", "Description"]
        print(tabulate(admin_options, headers=headers, tablefmt="grid", colalign=("center", "left")))

        self.options = {
            1:  self.admin.add_user,
            2:  self.admin.delete_user,
            3:  self.admin.add_menu,
            4:  self.admin.delete_menu,
            5:  self.admin.update_menu,
            6:  self.admin.update_price,
            7:  self.admin.user_info,
            8:  self.admin.menu_info,
            9:  self.admin.reset_password,
            10: self.admin.log_out,
            11: exit,
            12: self.admin.log_out,
            }
        
        while True:
            option = self.get_option(self.options)
            if option == 11:
                break

    def user_option(self):
        self.usermanager.login_interface()
        user_options = [
            ("1", "Update Username"),
            ("2", "Update Password"),
            ("3", "Delete Account"),
            ("4", "Log Out"),
            ("5", "Exit"),
            ("6", "Back"),
        ]

        headers = ["Option", "Description"]
        print(tabulate(user_options, headers=headers, tablefmt="grid", colalign=("center", "left")))
        
        self.options = {
            1:  self.usermanager.update_username,
            2:  self.usermanager.update_password,
            3:  self.usermanager.delete_account,
            4:  self.usermanager.log_out,
            5:  exit,
            6:  self.admin.log_out,
        }
        
        while True:
            option = self.get_option(self.options)
            if option == 6:
                break

    def guest_option(self):
        guest_options = [
            ("1", "Guest Login"),
            ("2", "Login"),
            ("3", "Sign in"),
            ("4", "Exit"),
            ("5", "Back"),
        ]

        headers = ["Option", "Description"]
        print(tabulate(guest_options, headers=headers, tablefmt="grid", colalign=("center", "left")))
        
        self.options = {
            1: self.usermanager.log_out, 
            2: self.usermanager.login_interface,
            3: self.usermanager.add_user,
            4: exit,
            5: self.admin.log_out,
        }
        
        while True:
            option = self.get_option(self.options)
            if option == 5:
                break