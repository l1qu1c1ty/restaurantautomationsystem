# main.py
# This script serves as the entry point for the restaurant automation system.
# It imports necessary modules and initializes the system components.
# The `RunSystem` class orchestrates the execution of the restaurant order system.
# The script handles user interaction, menu display, order processing, and more.
# It utilizes external libraries such as colorama for enhancing the user interface and logging_utils for error logging.

# Import necessary modules
from restaurantsystem import RestaurantOrderSystem
from os import system as command
from database_manager import DatabaseManager
from restaurant_interface import RestaurantOrderInterface
from colorama import Fore as color
import logging_utils
import os

logging_utils.setup_logging()

# Define the paths and directories for the application
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
user_folder = os.path.expanduser("~")
current_directory = os.getcwd()
db_file = "restaurant.db"
db_path = os.path.join(current_directory, app_dir, db_file)

# Define a class to run the restaurant automation system
class RunSystem:
    # Method to execute the restaurant automation system
    def run_script(self):
        try:
            # Initialize the database manager
            db_manager = DatabaseManager(db_path)

            # Initialize the user interface for the restaurant order system
            startui = RestaurantOrderInterface(db_manager)

            while True:
                # Clear the screen (for Windows)
                command("cls")

                # Display the main menu and handle user input
                startui.start_option()

                # Create an instance of the RestaurantOrderSystem
                order = RestaurantOrderSystem(db_manager)

                # Setup the database for menu items (sorted by price)
                order.setup_database(sort_by_price=True)

                # Display a greeting to the customer
                print(color.LIGHTGREEN_EX)
                order.salutation_customer()

                # Display the menu to the customer
                print(color.YELLOW)
                order.display_menu()

                # Allow the customer to make a menu selection
                order.customer_menu()

                # Process the payment for the order
                order.payment_process()

                # Ask if the customer wants to leave a tip
                order.waitress_tip()

                # Generate and display an invoice
                print(color.YELLOW)

                # Ask if the customer wants to exit the program
                exit_question = input("Exit (Q): ").upper()
                if exit_question == "Q":
                    break

                # Clear the screen and return to the main menu
                command("cls")
                startui.start_option()

        except KeyboardInterrupt as e:
            print("\n")
            print("Exiting the Program...")
            logging_utils.log_info(f"An error occurred: Keyboard Interrupt Ctrl+C")

        except EOFError as e:
            print("\n")
            print("Exiting the Program...")
            logging_utils.log_info(f"An error occurred: Keyboard Interrupt Ctrl+Z")

        except ValueError:
            print("Enter numerical option")
            logging_utils.log_error(f"An error occurred: Enter numerical option")

        except Exception as e:
            print(e)
            logging_utils.log_error(f"An error occurred: {e}")

# Define the main function to run the restaurant automation system
def main():
    main = RunSystem()
    main.run_script()

# Execute the main function if this script is the main entry point
if __name__ == "__main__":
    main()
