from restaurantsystem import *
from os import system as command
from database_manager import DatabaseManager

class RunSystem:
    def run_script(self):
        try:
            db_manager = DatabaseManager("../data/restaurant.db")
            startui = RestaurantOrderInterface(db_manager)
            while True:
                command("cls")
                startui.start_option()
    
                print(color.LIGHTGREEN_EX)
                order = RestaurantOrderSystem(db_manager)
                order.setup_database(sort_by_price=True)

                print(color.YELLOW)
                order.salutation_customer()

                print(color.LIGHTGREEN_EX)
                order.display_menu()
                order.customer_menu()
                order.payment_process()
                order.waitress_tip()
                order.discount_vouchers()

                print(color.YELLOW)
                order.invoice()
                exit_question = input("Exit (Q): ").upper()
                if exit_question == "Q":
                    break
                command("cls")
                startui.start_option()

        except KeyboardInterrupt:
            print("\n")
            print("Exiting the Program...")

        except EOFError:
            print("\n")
            print("Exiting the Program...")

        except Exception as e:
            print(e)

def main():
    main = RunSystem()
    main.run_script()

if __name__ == "__main__":
    main()