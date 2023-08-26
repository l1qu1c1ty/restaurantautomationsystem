# Restaurant Automation System
# Version 1.3.0
# Created by Melih Can Demir

# Importing necessary libraries
from pyfiglet import figlet_format as figlet
from colorama import Fore as color
from os import system as command
from time import sleep
from database_manager import DatabaseManager
#import sqlite3 as sql

# Restaurant Order and Payment Automation
class RestaurantOrderSystem():
    def __init__(self, database_manager):
        # Initialize menu dictionary and database connection variables
        self.menu = {}
        self.database_manager = database_manager
        self.name = str()

    def setup_database(self):
        try:
            # Connect to the database and fetch menu data
            self.database_manager.connect()
            self.menu_data = self.database_manager.fetch_all("SELECT name, price FROM menu")

            # Populate menu dictionary with menu items and prices
            for name, price in self.menu_data:
                self.menu[name] = price

        except Exception as e:
            print("An error occurred:", e)

    def customer_menu(self):
        while True:
            # Get customer's order input and validate it against the menu
            self.customer_order = input("Please enter order menu: ").capitalize()
            cleaned_order = self.customer_order.strip().lower()

            for menu_item, item_price in self.menu.items():
                if cleaned_order == menu_item.lower():
                    self.order_price = item_price
                    print("=" * 50)
                    print("The Menu: {} - ${}".format(self.customer_order, item_price))
                    print("=" * 50)
                    print("Thanks for your order, {}!".format(self.name))
                    print("Your order will be ready in ~10 minutes.")
                    print("=" * 50)
                    return

            else:
                print("Invalid menu. Please choose another item from the menu.")

    def display_menu(self):
        try:
            # Display the menu items and prices
            print("=" * 30)
            for index, (name, price) in enumerate(self.menu_data, start=1):
                print("{:<0}. {:<20} {:<5}$".format(index, name, price))
            print("=" * 30)

        except Exception as e:
            print("An error occurred:", e)

    def salutation_customer(self):
        # Welcome and ask for the customer's name
        print("Welcome Restaurant!\n")
        print("What are you eating or drinking today ?\n")
        self.name = input("Hello there! What is your name?\n\n")

    def payment_process(self):
        while True:
            try:
                # Get payment method and validate it
                self.payment_method = input("Cash or Creditcard:").capitalize()
                if self.payment_method == "Creditcard" or self.payment_method == "Cash":
                    self.customer_balance = float(
                        input("Enter the amount to pay $"))
                    prices = float(self.menu[self.customer_order])
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
        # It gives the price of the menu, the amount paid, tip, change and payment method information.
        self.change = self.customer_balance - \
            float(self.order_price) - self.customer_tip
        if self.change >= 0:
            separator = "-" * 50
            invoice_lines = [
                separator,
                "{:^50}".format("Restaurant Invoice"),
                "",
                "{:<30}${:.2f}".format(
                    self.customer_order, float(self.order_price)),
                separator,
                "{:<30}${:.2f}".format(
                    "Payment:", float(self.customer_balance)),
                "{:<30}${:.2f}".format("Tip:", float(self.customer_tip)),
                separator,
                "{:<30}${:.2f}".format("Change:", float(self.change)),
                "{:<30}{}".format("Payment Method:", str(self.payment_method)),
                separator,
            ]
            
            with open("invoice.txt","w") as file:
                for line in invoice_lines:
                    print(line)
                    line += "\n"
                    file.writelines(line)
        else:
            print("Insufficient payment for the order")

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
            login_data = [(username, password)]
            self.database_manager.executemany("""
                               INSERT INTO login (username, password)
                               VALUES (?, ?)""", login_data)
            
            self.database_manager.commit()
        
        except Exception as e:
            print("An error occurred while adding user:", e)
        

    def update_username(self):
        user_name = input("Enter the user name to update: ")
        new_username = input("Enter the new name for the menu: ")
        self.database_manager.execute("UPDATE login SET username = ? WHERE username = ?", (new_username, user_name))
        self.database_manager.commit()
        print("Username updated successfully!")
        
    def update_password(self):
        user_password = input("Enter the user password to update: ")
        new_password = input("Enter the new name for the menu: ")
        self.database_manager.execute("UPDATE login SET password = ? WHERE password = ?", (new_password, user_password))
        self.database_manager.commit()
        print("Password updated successfully!")
    
    def reset_password(self):
        pass

    def delete_account(self):
        pass
    
    def log_out(self):
        print("Log Out Progress...")
        sleep(2)
        return

class Admin(UserManager):
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def add_menu(self):
        menu_name = input("Enter menu name: ")
        menu_price = input("Enter menu price: ")
        menu_data = [(menu_name,menu_price)]
        self.database_manager.execute_query("""
                      INSERT INTO menu (name, price)
                      VALUES (?, ?)
                      """, menu_data)
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
        self.database_manager.execute_query("SELECT * FROM login")
        users = self.database_manager.fetch_all()
        for user in users:
            print("="*50)
            print("\n".join(user))
            print("="*50)

class RestaurantOrderInterface:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.restaurant = RestaurantOrderSystem(self.database_manager)
        self.usermanager = UserManager(self.database_manager, self)
        self.admin = Admin(self.database_manager)

    def start_option(self):
        print(color.GREEN)
        print(figlet("Welcome Restaurant"))
        print(color.LIGHTGREEN_EX)
        startup = """
        ------ Welcome -----
        1. - Login         -
        2. - Sign in       -
        3. - Guest         -
        4. - Admin         -
        5. - User          -
        6. - Exit          -
        ---- Restaurant ----
        """
        print(startup)

        self.options = {
            1: self.usermanager.login_interface,
            2: self.usermanager.add_user,
            3: self.guest_option,
            4: self.admin_option,
            5: self.user_option,
            6: exit,
        }
        
        while True:
            startup_option = input("Enter option number: ")
            if startup_option.isdigit():
                option_number = int(startup_option)
                selected_option = self.options.get(option_number)
                if selected_option:
                    selected_option()
                    command("cls")
                    break
                else:
                    print("Error! Please enter a valid option number.")
                
            else:
                print("Error! Please enter a valid number.")
            
    def admin_option(self):
        self.usermanager.login_interface()
        admin_opt = """
        --- Admin Option ----
        1. - Add User       -
        2. - Delete User    - 
        3. - Add Menu       -
        4. - Delete Menu    -
        5. - Update Menu    -
        6. - Update Balance -
        7. - Show Users     -
        8. - Log Out        -
        9. - Exit           -
        10.- Back           -
        ------- Admin -------
        """
        print(admin_opt)

        self.options = {
            1:  self.admin.add_user,
            2:  self.admin.delete_user,
            3:  self.admin.add_menu,
            4:  self.admin.delete_menu,
            5:  self.admin.update_menu,
            6:  self.admin.update_price,
            7:  self.admin.user_info,
            8:  self.admin.log_out,
            9:  exit,
            10: self.start_option,
        }
        admin_question = input("Enter option: ")
        if admin_question.isdigit():
            option_number = int(admin_question)
            selected_option = self.options.get(option_number)
            if selected_option:
                selected_option()
                command("cls")
            else:
                print("Error! Please enter a valid option number.")
        else:
            print("Error! Please enter a valid number.")

    def user_option(self):
        self.usermanager.login_interface()
        user_opt = """
        -- User Option --
        1. - Update Username -
        2. - Update Password -
        3. - Delete Account  -
        4. - Log Out         -
        5. - Exit            -
        6. - Back            -
        """
        print(user_opt)
        self.options = {
            1:  self.usermanager.update_username,
            2:  self.usermanager.update_password,
            3:  self.usermanager.delete_account,
            4:  self.usermanager.log_out,
            5:  exit,
            6:  self.start_option,
        }
        user_question = input("Enter option: ")
        if user_question.isdigit():
            option_number = int(user_question)
            selected_option = self.options.get(option_number)
            if selected_option:
                selected_option()
                sleep(2)
                command("cls")
            else:
                print("Error! Please enter a valid option number.")
        else:
            print("Error! Please enter a valid number.")

    def guest_option(self):
        guest_opt = """
        -- Guest Option --
        1. - Login   -
        2. - Sign in -
        3. - Exit    -
        4. - Back    -
        """
        print(guest_opt)
        self.options = {
            1: self.usermanager.login_interface,
            2: self.usermanager.add_user,
            3: exit,
            4: self.start_option,
        }
        guest_question = input("Enter option:")
        if guest_question.isdigit():
            option_number = int(guest_question)
            selected_option = self.options.get(option_number)
            if selected_option:
                selected_option()
                command("cls")
            else:
                print("Error! Please enter a valid option number.")
        else:
            print("Error! Please enter a valid number.")

def main():
    try:
        db_manager = DatabaseManager("restaurant.db")
        while True:
            command("cls")
            startui = RestaurantOrderInterface(db_manager)
            startui.start_option()
    
            print(color.LIGHTGREEN_EX)
            order = RestaurantOrderSystem(db_manager)
            order.setup_database()

            print(color.YELLOW)
            order.salutation_customer()

            print(color.LIGHTGREEN_EX)
            order.display_menu()
            order.customer_menu()
            order.payment_process()
            order.waitress_tip()

            print(color.YELLOW)
            order.invoice()
            exit_question = input("Exit (Q): ").upper()
            if exit_question == "Q":
                break
            command("cls")

    except KeyboardInterrupt:
        print("\n")
        print("Exiting the Program...")

    except EOFError:
        print("\n")
        print("Exiting the Program...")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()