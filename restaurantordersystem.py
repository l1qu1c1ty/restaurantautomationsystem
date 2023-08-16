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
            'Fries':         19.99,
            'Sandwich':      24.99,
            'Cheeseburger':  14.99,
            'Coffee':         7.99,
            'Soda':           4.99,
        }

    # Specifies customer order
    def customer(self, order):
        try:
            print("="*50)
            print(f"The Menu: {order} - {self.menu[order]}$")
            print("="*50)

        except KeyError:
            print("Item not found in the menu.")

        else:
            print(f"Thanks for your order. {self.name}")
            print("Your order will be ready in ~10 minutes.")
            print("="*50)

    # Displays the menu on the screen
    def display_menu(self):
        print("="*30)
        for index, food in enumerate(self.menu, start=1):
            price = self.menu[food]
            print("{:<0}. {:<20} {:<10}".format(index, food, price))
        print("="*30)

    # Welcome Message to Customer
    def greeting(self):
        print("Welcome Restaurant!\n")
        print("What are you eating or drinking today ?\n")

    # An empty payment function but this will be completed in the future
    def payment(self):
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
        customers_order = input("Please enter order menu: ")
        order.customer(customers_order)
        input()
        command("cls")

    except Exception as e:
        print(e)

# If the function name is main, it executes the code inside the main function.
if __name__ == "__main__":
    main()
