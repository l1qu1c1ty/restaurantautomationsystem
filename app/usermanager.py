# usermanager.py
# This module contains the implementation of the 'UserManager' class, responsible for managing user-related actions,
# and the 'Guest' class, which provides functionality for guest sessions.
# The 'UserManager' class handles user authentication, user account management, and password encryption.
# It allows users to log in, add users, update usernames and passwords, reset passwords, and delete accounts.
# The 'Guest' class is used for guest sessions and provides access to the menu without user authentication.
# The module also includes a function to generate random passwords and uses the 'bcrypt' library for password hashing.

# Import necessary modules
import bcrypt
import pwinput
import logs_utils
import string
import random

# Set up logging for error handling
logs_utils.setup_logging()

# Function to generate a random password
def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(random.choice(characters) for _ in range(length))
    return random_password

# Define the 'UserManager' class for user authentication and account management
class UserManager:
    def __init__(self, database_manager, restaurant_order_interface):
        self.database_manager = database_manager
        self.restaurant_order_interface = restaurant_order_interface

    # Method to handle user login
    def login_interface(self):
        max_attempts = 3
   
        while max_attempts > 0:
            try:
                # Prompt the user for username and password
                self.database_manager.connect()
                self.username = input("Username: ")
                self.password = pwinput.pwinput("Password: ")
                self.database_manager.execute_query("SELECT username, password FROM login WHERE username = ?", (self.username,))
                row = self.database_manager.cursor.fetchone()
                if row:
                    db_username, db_hashed_password = row
                    # Check if the entered password matches the stored hashed password
                    if self.username == db_username and bcrypt.checkpw(self.password.encode('utf-8'), db_hashed_password):
                        print("You have successfully logged in!")
                        break

                    else:
                        print("Incorrect username or password.")
                        max_attempts -= 1
                else:
                    print("Incorrect username or password.")
                    max_attempts -= 1
            
            except Exception as e:
                print("An error occurred:", e)
                logs_utils.log_error(f"An error occurred: {e}")
        
        if max_attempts == 0:
            print("Too many incorrect attempts. Returning to the main menu.")
            self.restaurant_order_interface.start_option()
    
    # Method to add a new user to the system
    def add_user(self):
        try:
            username = input("Enter Username: ")
            password = pwinput.pwinput("Enter Password: ")

            # Hash the password before storing it in the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            login_data = (username, hashed_password)
            self.database_manager.execute_query("INSERT INTO login (username, password) VALUES (?, ?)", login_data)
            self.database_manager.commit()
            print("User added successfully!")
        
        except Exception as e:
            print("An error occurred while adding user:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to update a user's username
    def update_username(self):
        old_username = input("Enter the old username: ")

        # Check if the old username exists in the database
        self.database_manager.execute_query("SELECT username FROM login WHERE username = ?", (old_username,))
        row = self.database_manager.cursor.fetchone()

        if row:
            new_username = input("Enter the new username: ")
            self.database_manager.execute_query("UPDATE login SET username = ? WHERE username = ?", (new_username, old_username))
            self.database_manager.commit()
            print("Username updated successfully!")
        
        else:
            print("Old username not found. Username update failed.")
        
    # Method to update a user's password
    def update_password(self):
        username = input("Enter your username: ")

        # Check if the username exists in the database
        self.database_manager.execute_query("SELECT password FROM login WHERE username = ?", (username,))
        row = self.database_manager.cursor.fetchone()

        if row:
            old_password = pwinput.pwinput("Enter your old password: ")
            db_hashed_password = row[0]

            if bcrypt.checkpw(old_password.encode('utf-8'), db_hashed_password):
                new_password = pwinput.pwinput("Enter your new password: ")
                
                # Encrypt the new password with bcrypt
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Update the password in the database
                self.database_manager.execute_query("UPDATE login SET password = ? WHERE username = ?", (hashed_password, username))
                self.database_manager.commit()
                print("Password updated successfully!")
            
            else:
                print("Incorrect old password. Password update failed.")
        else:
            print("User not found. Password update failed.")
    
    # Method to reset a user's password
    def reset_password(self):
        try:
            username = input("Enter the username for which you want to reset the password: ")

            # Check if the username exists in the database
            self.database_manager.execute_query("SELECT username FROM login WHERE username = ?", (username,))
            row = self.database_manager.cursor.fetchone()

            if row:
                new_password = generate_random_password()  # Generate a random password 

                # Hash and salt the new password with bcrypt
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                self.database_manager.execute_query("UPDATE login SET password = ? WHERE username = ?", (hashed_password, username))
                self.database_manager.commit()

                print(f"The password for user {username} has been reset. The new password is: {new_password}")
            else:
                print("User not found. Password reset failed.")

        except Exception as e:
            print("An error occurred while resetting password:", e)
            logs_utils.log_error(f"An error occurred: {e}")

    # Method to delete a user account
    def delete_account(self):
        try:
            username = input("Enter your username to confirm account deletion: ")

            # Check if the username exists in the database
            self.database_manager.execute_query("SELECT username FROM login WHERE username = ?", (username,))
            row = self.database_manager.cursor.fetchone()

            if row:
                confirmation = input(f"Are you sure you want to delete the account '{username}'? (Y/N): ").strip().lower()
                if confirmation == 'y':
                    self.database_manager.execute_query("DELETE FROM login WHERE username = ?", (username,))
                    self.database_manager.commit()
                    print(f"User '{username}' has been successfully deleted.")
                else:
                    print("Account deletion canceled.")
            else:
                print("User not found. Account deletion failed.")

        except Exception as e:
            print("An error occurred while deleting the account:", e)
            logs_utils.logging.error(f"An error occurred: {e}")
    
    # Method to log out a user
    def log_out(self):
        try:
            if self.username:
                # Provide a logout confirmation message
                print(f"User {self.username} has been successfully logged out.")
            else:
                print("No user session found. You were not logged in.")

            # Redirect or return to the main menu
            self.restaurant_order_interface.start_option()

        except Exception as e:
            print("An error occurred during logout:", e)
            logs_utils.logging.error(f"An error occurred: {e}")

# Define the 'Guest' class for guest sessions
class Guest(UserManager):
    def __init__(self):
        pass
    
    # Method for guest login, allowing access to the menu without authentication
    def guest_login(self, restaurant_order_system):
        print("Welcome to the Guest Session!")
        restaurant_order_system.setup_database()
        restaurant_order_system.display_menu()
