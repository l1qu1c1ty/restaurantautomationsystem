# Restaurant Order and Payment Automation
# Importing Library
from pyfiglet import figlet_format as figlet
from colorama import Fore as color
from os import system as command
import sqlite3 as sql
# Here is the Class name RestaurantMenu
class RestaurantOrderSystem():
    # Instance Constructor
    def __init__(self, name):
        self.name = name
        self.menu = {}

        try:
            self.connection = sql.connect("restaurant.db")
            self.c = self.connection.cursor()
            self.c.execute("SELECT name, price FROM menu")
            self.menu_data = self.c.fetchall()

            for name, price in self.menu_data:
                self.menu[name] = price

        except sql.Error as e:
            print("An error occurred while fetching the menu:", e)

    # Specifies customer order
    def customer(self, order):
        while True:
            price = self.menu.get(order)
            if price is not None:
                self.order = order
                self.order_price = price
                print("=" * 50)
                print("The Menu: {} - ${}".format(order, price))
                print("=" * 50)
                print("Thanks for your order, {}!".format(self.name))
                print("Your order will be ready in ~10 minutes.")
                print("=" * 50)
                break
            
            else:
                print("Invalid menu. Please choose another item from the menu.")
                order = input("Please enter a valid order menu: ").capitalize()

    # Displays the menu on the screen
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

    # An empty payment function but this will be completed in the future
    def payment(self, payment_method, balance):
        prices = float(self.menu[self.order])
        self.balance = balance
        if payment_method == "Creditcard":
            if balance >= prices:
                balance -= prices - self.tip
                print("Payment Confirmed.")
                print("Thank you for choosing us.")
                print("Have a nice day!")
            else:
                print("Insufficient Balance!")
                print("Please Try Again or Change Payment Method!")
        
        elif payment_method == "Cash":
            if balance >= prices:
                balance -= prices - self.tip
                print("Thanks for your payment!")
                print("Thank you for choosing us.")
                print("Have a nice day!")
            else:
                print("Insufficient Balance!")
                print("Please Try Again or Change Payment Method!")
    
    # Will be arranged soon for refund system
    def refund(self):
        pass    
    
    def waitress_tips(self, tip=0, balance=0):
        self.tip = tip
        print("-"*50)
        if balance >= float(self.order_price) + self.tip and tip >= 0:
            print(f"{self.name} Thanks for the tips.")
            print(f"Tip: {tip}")
        
        else:
            print("Balance is not enough to pay the tip insufficient!")
            print(f"Tip is invalid! ${int(tip)}")
        print("-"*50)
    
    def invoice(self, payment_method):
        self.change = self.balance - float(self.order_price) - self.tip
        if self.change >= 0:
            separator = "-" * 50
            invoice_lines = [
            separator,
            "{:^50}".format("Restaurant Invoice"),
            "",
            "{:<30}${:.2f}".format(self.order, float(self.order_price)),
            separator,
            "{:<30}${:.2f}".format("Payment:", float(self.balance)),
            "{:<30}${:.2f}".format("Tip:", float(self.tip)),
            separator,
            "{:<30}${:.2f}".format("Change:", float(self.change)),
            "{:<30}{}".format("Payment Method:", str(payment_method)),
            separator,
            ]
            print("\n".join(invoice_lines))

    def login_interface(self, username, password):
        try:
            self.c.execute("SELECT username, password FROM login WHERE username = ?", (username,))
            row = self.c.fetchone()

            if row:
                db_username, db_password = row
                if (username == db_username and password == db_password):
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

# Here is the Main Function
def main():
    try:
        while True:
            print(color.LIGHTGREEN_EX)
            print(figlet("Welcome Restaurant"))
            greeting = RestaurantOrderSystem("")
            print(color.YELLOW)
            greeting.greeting()
            customer_name = input("Hello there! What's your name ? \n\n")
            print(color.LIGHTBLUE_EX)
            order = RestaurantOrderSystem(customer_name)   
            username = input("Username: ")
            password = input("Password: ")
            order.login_interface(username, password)
            order.display_menu()
            print(color.LIGHTGREEN_EX)
            customers_order = input("Please enter order menu: ").capitalize()
            order.customer(customers_order)
            customer_payment = input("How would you like to make your payment ? ").capitalize()
            customer_balance = float(input("Enter the amount to pay: "))
            customer_tip = float(input("Would you like to tip? (default = 0): "))
            order.waitress_tips(customer_tip, customer_balance)
            order.payment(customer_payment, customer_balance)
            order.invoice(customer_payment)
            exit_question = input("Exit (Q): ").upper()
            if exit_question == "Q":
                break
            command("cls")

    except Exception as e:
        print(e)

# If the function name is main, it executes the code inside the main function.
if __name__ == "__main__":
    main()