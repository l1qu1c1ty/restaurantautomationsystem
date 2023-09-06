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
import pkg_resources

# Define the 'app' directory path and add it to the system path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(app_dir)


def clear_screen():
    # Determine the current operating system
    if os.name == 'posix':  # Linux and Unix-like systems
        os.system('clear')
    
    elif os.name == 'nt':   # Windows
        os.system('cls')
    
    else:
        # Other or unsupported operating systems
        print("Screen clearing is not supported on this platform.")

# Call the clear_screen() function to clear the screen
clear_screen()

def is_package_installed(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        return True
    
    except pkg_resources.DistributionNotFound:
        return False

# Method to display package requirements from 'requirements.txt' as a table
def display_requirements():
    with open("requirements.txt", "r") as f:
        # Skip the first line in requirements.txt
        next(f)

        # Print a header row
        print("-" * 50)
        print("{:<20} {:<15}".format("Package", "Status"))
        print("-" * 50)
        
        # Iterate through the lines in requirements.txt
        for line in f.readlines():
            # Split each line into package and version (if available)
            parts = line.strip().split("==")
            
           # Extract package and version
            package = parts[0].strip()
            
            # Check if the package is installed
            is_installed = is_package_installed(package)
            
            # Determine the status (installed or not)
            status = "Installed" if is_installed else "Not Installed"
            
            # Print the package and version in a formatted table-like manner
            print("{:<20} {:<10}".format(package, status))
            
        print("-" * 50)
        f.close()

# Define an 'Install' class to manage package installation and application execution
class Install():
    # Method to display package requirements from 'requirements.txt' and prompt for installation
    def requirements(self):
        # Call the display_requirements() function to display the requirements as a table
        display_requirements()
        
        question = input("\nDo you want to install packages Yes (Y) / No (N):").strip().upper()
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
        question2 = input("\nDo you want to run the application Yes (Y) /No (N):").strip().upper()
        if question2 == "Y":
            # Import the 'main' function from 'app.main'
            from app.main import main as main_app   # Solution
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