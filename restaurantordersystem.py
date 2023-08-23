# Restaurant Order and Payment Automation
from pyfiglet import figlet_format as figlet
from colorama import Fore as color
from os import system as command
import sqlite3 as sql

class RestaurantOrderSystem():
    def __init__(self):
        self.menu = {}
        self.connection = None
        self.c = None
    
    def setup_database(self):
        try:
            self.connection = sql.connect("restaurant.db")
            self.c = self.connection.cursor()
            self.c.execute("SELECT name, price FROM menu")
            self.menu_data = self.c.fetchall()

            for name, price in self.menu_data:
                self.menu[name] = price
        
        except sql.Error as e:
            print("An error occurred while fetching the menu:", e)

    def customer(self):
        while True:
            self.customer_order = input("Please enter order menu: ").capitalize()
            cleaned_order = self.customer_order.strip().lower()
            
            price = None
            for menu_item, item_price in self.menu.items():
                if cleaned_order == menu_item.lower():
                    price = item_price
                    break

            if price is not None:
                self.order_price = price
                print("=" * 50)
                print("The Menu: {} - ${}".format(self.customer_order, price))
                print("=" * 50)
                print("Thanks for your order, {}!".format(self.name))
                print("Your order will be ready in ~10 minutes.")
                print("=" * 50)
                break
            
            else:
                print("Invalid menu. Please choose another item from the menu.")

    def display_menu(self):
        try:
            print("=" * 30)
            for index, (name, price) in enumerate(self.menu_data, start=1):
                print("{:<0}. {:<20} {:<5}$".format(index, name, price))
            print("=" * 30)

        except sql.Error as e:
            print("An error occurred:", e)

    # Welcome Message to Customer
    def greeting(self):
        print("Welcome Restaurant!\n")
        print("What are you eating or drinking today ?\n")
        self.name = input("Hello there! What is your name?\n\n")

    def payment(self):
        while True:
            self.payment_method = input("Cash or Creditcard:").capitalize()
            if self.payment_method == "Creditcard" or self.payment_method == "Cash":
                self.customer_balance = float(input("Enter the amount to pay $"))
                prices = float(self.menu[self.customer_order])
                if self.customer_balance >= prices:
                    print("Payment Confirmed.")
                    break
                else:
                    print("Insufficient Balance!")
                    print("Please Try Again or Change Payment Method!")
                    break   
            else:
                print("Invalid Payment Method!")

    def waitress_tips(self):
        self.customer_tip = float(input("Would you like to tip $"))
        print("-"*50)
        if self.customer_balance >= float(self.order_price) + self.customer_tip and self.customer_tip >= 0:
            print(f"{self.name} Thanks for the tips.")
            print(f"Tip: ${self.customer_tip:.2f}")
            print("Thank you for choosing us.")
            print("Have a nice day!")
        else:
            print("Balance is not enough to pay the tip.")
            print(f"Tip is invalid: ${self.customer_tip:.2f}")
        print("-"*50)
    
    def invoice(self):
        self.change = self.customer_balance - float(self.order_price) - self.customer_tip
        if self.change >= 0:
            separator = "-" * 50
            invoice_lines = [
            separator,
            "{:^50}".format("Restaurant Invoice"),
            "",
            "{:<30}${:.2f}".format(self.customer_order, float(self.order_price)),
            separator,
            "{:<30}${:.2f}".format("Payment:", float(self.customer_balance)),
            "{:<30}${:.2f}".format("Tip:", float(self.customer_tip)),
            separator,
            "{:<30}${:.2f}".format("Change:", float(self.change)),
            "{:<30}{}".format("Payment Method:", str(self.payment_method)),
            separator,
            ]
            
            for line in invoice_lines:
                print(line)
        
        else:
            print("Insufficient payment for the order")
    
    def login_interface(self):
        try:
            self.username = input("Username: ")
            self.password = input("Password: ")
            self.c.execute("SELECT username, password FROM login WHERE username = ?", (self.username,))
            row = self.c.fetchone()

            if row:
                db_username, db_password = row
                if (self.username == db_username and self.password == db_password):
                    print("Welcome {}".format(self.name))
                    print("You have successfully logged in!")
                else:
                    print("Incorrect password.")
                    print("Continuing with Guest account!")
            else:
                print("User not found.")
                print("Continuing with Guest account.")
        
        except sql.Error as e:
            print("An error occurred:", e)
        
        finally:
            self.connection.close()

def main():
    try:
        while True:
            command("cls")
            print(color.LIGHTGREEN_EX)
            print(figlet("Welcome Restaurant"))    
            
            print(color.LIGHTBLUE_EX)
            order = RestaurantOrderSystem()
            order.setup_database()
            
            print(color.YELLOW)
            order.greeting()
            order.login_interface()
            
            print(color.LIGHTGREEN_EX)
            order.display_menu()
            order.customer()
            order.payment()
            order.waitress_tips()
            
            print(color.LIGHTWHITE_EX)
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