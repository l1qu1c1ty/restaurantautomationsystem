# setup.py
# This script is used to install required packages and run the restaurant automation system.
# It appends the 'app' directory to the system path to make it accessible.
# The `Install` class provides methods to install packages listed in 'requirements.txt' and run the main application.
# Users are prompted to confirm the installation and execution.
# It utilizes the 'os' and 'sys' modules for system operations and interacts with the main application using 'main_app' from 'app.main'.

# Import necessary modules
from os import system as command
import os
import sys

# Define the 'app' directory path and add it to the system path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(app_dir)

# Import the 'main' function from 'app.main'
from app.main import main as main_app

# Clear the screen (for Windows)
command("cls")

# Define an 'Install' class to manage package installation and application execution
class Install():
    # Method to display package requirements from 'requirements.txt' and prompt for installation
    def requirements(self):
        with open("requirements.txt", "r") as f:
            for file in f.readlines():
                print(file)
            
            f.close()
        
        question = input("\nDo you want to install packages Y/N:").strip().upper()
        if question == "Y":
            command("pip install -r requirements.txt")
            print("# Successfully installed. #")
        
        elif question == "N":
            print("User canceled install packages!")
            sys.exit(0)
        
        else:
            print("User canceled install packages!")
            sys.exit(0)
    
    # Method to prompt for running the main application
    def run_script(self):
        question2 = input("\nDo you want to run the application Y/N:").strip().upper()
        if question2 == "Y":
            main_app()
        
        elif question2 == "N":
            print("User canceled run main.py")
        
        else:
            print("User canceled run main.py")
            sys.exit(0)

# Define the main function to install packages and run the application
def main():
    install = Install()
    install.requirements()
    install.run_script()

# Execute the main function if this script is the main entry point
if __name__ == "__main__":
    main()