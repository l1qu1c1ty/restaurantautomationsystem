# admin.py
# This module contains the implementation of the 'Admin' class, which extends 'UserManager'.
# The 'Admin' class is responsible for handling administrative actions in the restaurant order system.
# It allows administrators to add, delete, update menu items, delete users, and view user information.
# Additionally, administrators can update menu item prices.
# The module utilizes the 'tabulate' library for user-friendly tabular displays and 'logging_utils' for error logging.

# Import necessary modules
from restaurantsystem import RestaurantOrderSystem
from usermanager import UserManager
from tabulate import tabulate
import logs_utils

# Set up logging for error handling
logs_utils.setup_logging()

# Define the 'Admin' class, which extends 'UserManager'
class Admin(UserManager):
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.restaurant = RestaurantOrderSystem(database_manager)

    # Method to add a new menu item to the system
    def add_menu(self):
        try:
            menu_name = input("Enter menu name: ")
            menu_price = input("Enter menu price: ")
            menu_data = (menu_name, menu_price)
            self.database_manager.execute_query("INSERT INTO menu (name, price) VALUES (?, ?)", menu_data)
            self.database_manager.commit()
            print("Menu item added successfully!")

        except Exception as e:
            print("An error occurred while adding menu item:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to delete a menu item from the system
    def delete_menu(self):
        try:
            menu_name = input("Enter menu name: ")
            self.database_manager.execute_query("SELECT name FROM menu WHERE name = ?", (menu_name,))
            row = self.database_manager.cursor.fetchone()

            if row:
                confirmation = input(f"Do you really want to delete the menu item {menu_name}? (Y/N): ").strip().lower()
                if confirmation == 'y':
                    self.database_manager.execute_query("DELETE FROM menu WHERE name = ?", (menu_name,))
                    self.database_manager.commit()
                    print(f"Menu item '{menu_name}' deleted successfully.")
                else:
                    print("Menu item deletion canceled.")
            else:
                print("Menu item not found. Deletion failed.")

        except Exception as e:
            print("An error occurred while deleting menu item:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to delete a user from the system
    def delete_user(self):
        try:
            username = input("Enter username: ")
            self.database_manager.execute_query("SELECT username FROM login WHERE username = ?", (username,))
            row = self.database_manager.cursor.fetchone()

            if row:
                confirmation = input(f"Do you really want to delete the user {username}? (Y/N): ").strip().lower()
                if confirmation == 'y':
                    self.database_manager.execute_query("DELETE FROM login WHERE username = ?", (username,))
                    self.database_manager.commit()
                    print(f"User '{username}' deleted successfully.")
                else:
                    print("User deletion canceled.")
            else:
                print("User not found. Deletion failed.")

        except Exception as e:
            print("An error occurred while deleting user:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to update the name of a menu item
    def update_menu(self):
        try:
            menu_name = input("Enter the menu name to update: ")
            new_name = input("Enter the new name for the menu: ")
            
            self.database_manager.execute_query("SELECT name FROM menu WHERE name = ?", (menu_name,))
            row = self.database_manager.cursor.fetchone()

            if row:
                confirmation = input(f"Do you really want to update the menu item {menu_name}? (Y/N): ").strip().lower()
                if confirmation == 'y':
                    self.database_manager.execute_query("UPDATE menu SET name = ? WHERE name = ?", (new_name, menu_name))
                    self.database_manager.commit()
                    print("Menu item updated successfully!")
                else:
                    print("Menu item update canceled.")
            else:
                print("Menu item not found. Update failed.")

        except Exception as e:
            print("An error occurred while updating menu item:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to update the price of a menu item
    def update_price(self):
        try:
            menu_name = input("Enter the menu name to update price: ")
            new_price = input("Enter the new price $")

            self.database_manager.execute_query("SELECT name FROM menu WHERE name = ?", (menu_name,))
            row = self.database_manager.cursor.fetchone()

            if row:
                confirmation = input(f"Do you really want to update the price for menu item {menu_name}? (Y/N): ").strip().lower()
                if confirmation == 'y':
                    self.database_manager.execute_query("UPDATE menu SET price = ? WHERE name = ?", (new_price, menu_name))
                    self.database_manager.commit()
                    print("Menu price updated successfully!")
                else:
                    print("Menu price update canceled.")
            else:
                print("Menu item not found. Update failed.")

        except Exception as e:
            print("An error occurred while updating menu price:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to fetch and display user information
    def user_info(self):
        try:
            self.database_manager.execute_query("SELECT * FROM login")
            users = self.database_manager.fetch_all("SELECT * FROM login")
            headers = ["Username", "Password"]
            user_info_table = [[user[0], "*" * len(user[1])] for user in users]
            print(tabulate(user_info_table, headers=headers, tablefmt="fancy_grid"))

        except Exception as e:
            print("An error occurred while fetching user information:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to display menu information
    def menu_info(self):
        self.restaurant.setup_database()
        self.restaurant.display_menu()
