# Restaurant Order and Payment Automation
# Importing Library
from pyfiglet import figlet_format as figlet
from colorama import Fore as color
from os import system as command

# Here is the Class name RestaurantMenu
class RestaurantOrderSystem():
    # Instance Constructor
    def __init__(self, name):
        self.name = name
        self.menu = {
            'Cheeseburger':  24.99,
            'Sandwich':      19.99,
            'Fries':         16.99,
            'Coffee':        12.99,
            'Soda':          10.99,
        }

    # Specifies customer order
    def customer(self, order):
        try:
            self.order = order # Store the order as an attribute
            print("="*50)
            print(f"The Menu: {order} - ${self.menu[order]:.2f}")
            print("="*50)

        except KeyError:
            print("Please choose another item from the menu.")

        else:
            print(f"Thanks for your order. {self.name}")
            print("Your order will be ready in ~10 minutes.")
            print("="*50)

    # Displays the menu on the screen
    def display_menu(self):
        print("="*30)
        for index, food in enumerate(self.menu, start=1):
            price = self.menu[food]
            print("{:<0}. {:<20} {:<5}$".format(index, food, price))
        print("="*30)

    # Welcome Message to Customer
    def greeting(self):
        print("Welcome Restaurant!\n")
        print("What are you eating or drinking today ?\n")

    # An empty payment function but this will be completed in the future
    def payment(self, payment_method, balance):
        if payment_method == "Creditcard":
            if balance >= self.menu[self.order]:
                balance -= self.menu[self.order]
                print("Payment Confirmed.")
                print("Thank you for choosing us.")
                print("Have a nice day!")
            else:
                print("Insufficient Balance!")
                print("Please Try Again or Change Payment Method!")
        elif payment_method == "Cash":
            if balance >= self.menu[self.order]:
                balance -= self.menu[self.order]
                print("Thanks for your payment!")
                print("Thank you for choosing us.")
                print("Have a nice day!")
            else:
                print("Insufficient Balance!")
                print("Please Try Again or Change Payment Method!")
    
    # Will be arranged soon for refund system
    def refund():
        pass    
    
    # Will be arranged soon for the waiter tip system
    def waitress_tips():
        pass
    
    # Will be arranged soon for the invoice system
    def invoice():
        pass


    def login_interface(self, username, password):
        admin = "Micheal"
        admin_password = "1Sw0rd!2023"
        if username == admin and password == admin_password:
            print(f"Welcome {self.name}")
            print("You have successfully logged in!")

        elif username == "" or password == "":
            print("Welcome Guest")

        else:
            print("You entered the username or password incorrectly.")
            print("Continuing with Guest session.Thank you")

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
            order.payment(customer_payment,customer_balance)
            exit_question = input("Exit (Q): ").upper()
            if exit_question == "Q":
                break
            command("cls")

    except Exception as e:
        print(e)

# If the function name is main, it executes the code inside the main function.
if __name__ == "__main__":
    main()
