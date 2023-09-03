# restaurant_interface.py
# This module provides the command-line interface for a restaurant order system.
# It allows users to log in, sign up, and access different functionalities based on their roles.
# The interface includes options for guests, users, and administrators.
# Users can perform actions like updating their profile, ordering from the menu, and logging out.
# Administrators have additional functionalities like managing users and the restaurant's menu.
# It utilizes external libraries such as colorama, pyfiglet, and tabulate for improved user experience.
# Logging is also set up to capture errors for debugging purposes.

from restaurantsystem import RestaurantOrderSystem
from admin import Admin
from usermanager import UserManager
from usermanager import Guest
from colorama import Fore as color
from pyfiglet import figlet_format as figlet
from tabulate import tabulate
import logging_utils

logging_utils.setup_logging()

class RestaurantOrderInterface:
    # Initialize the interface with database manager and various system components.
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.restaurant = RestaurantOrderSystem(self.database_manager)
        self.usermanager = UserManager(self.database_manager, self)
        self.admin = Admin(self.database_manager)
        self.guest = Guest()

    # Method to get the selected option from the user.
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
                    logging_utils.log_error(f"An error occurred: Enter numerical option")
            else:
                print("Error! Please enter a valid number.")
                logging_utils.log_error(f"An error occurred: Enter numerical option")

    # Start the main option menu for users.
    def start_option(self):
        print(color.GREEN)
        print(figlet("Automation System",font="univers",width=120))
        print(color.LIGHTGREEN_EX)
        
        startup_options = [
            ("1", "Login"),
            ("2", "Sign up"),
            ("3", "Guest Session"),
            ("4", "Admin Session"),
            ("5", "User Session"),
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
            
    # Menu for the admin user.
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
            ("11","Back"),
            ("12","Exit"),        
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
            10: self.usermanager.log_out,
            11: self.start_option,
            12: exit,  
            }
        
        while True:
            option = self.get_option(self.options)
            if option == 11:
                break

    # Menu for regular users.
    def user_option(self):
        self.usermanager.login_interface()
        user_options = [
            ("1", "Update Username"),
            ("2", "Update Password"),
            ("3", "Delete Account"),
            ("4", "Log Out"),
            ("5", "Back"),
            ("6", "Exit"),
        ]

        headers = ["Option", "Description"]
        print(tabulate(user_options, headers=headers, tablefmt="grid", colalign=("center", "left")))
        
        self.options = {
            1:  self.usermanager.update_username,
            2:  self.usermanager.update_password,
            3:  self.usermanager.delete_account,
            4:  self.usermanager.log_out,
            5:  self.start_option,
            6:  exit,
        }
        
        while True:
            option = self.get_option(self.options)
            if option == 6:
                break

    # Menu for guest users.
    def guest_option(self):
        guest_options = [
            ("1", "Guest Login"),
            ("2", "Login"),
            ("3", "Sign up"),
            ("4", "Back"),
            ("5", "Exit"),   
        ]

        headers = ["Option", "Description"]
        print(tabulate(guest_options, headers=headers, tablefmt="grid", colalign=("center", "left"))) 
        self.options = {
            1: lambda: self.guest.guest_login(self.restaurant), 
            2: self.usermanager.login_interface,
            3: self.usermanager.add_user,
            4: self.start_option,
            5: exit,
        }
        
        while True:
            option = self.get_option(self.options)            
            
            if option == 5:
                break
