# test_database_manager.py
import sys
import os
import pytest

# Add the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app'))
sys.path.insert(0, root_dir)

# Import the DatabaseManager class from database_manager.py
from database_manager import DatabaseManager

import sqlite3

# Define a fixture to set up the test database
@pytest.fixture(scope="function")
def setup_test_database():
    # Create a connection to the test database
    conn = sqlite3.connect("test.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table (if it doesn't exist)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            column1 TEXT,
            column2 TEXT
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a DatabaseManager instance connected to the test database
    return DatabaseManager("test.db")

# Define the test function
def test_insert_data(setup_test_database):
    # Get the DatabaseManager instance from the fixture
    db_manager = setup_test_database

    # Insert test data into the database
    result = db_manager.execute_query("INSERT INTO my_table (column1, column2) VALUES (?, ?)", ("value1", "value2"))

    # Check if the insertion was successful (assuming your execute_query method returns a result)
    assert result == "Success", "Insertion failed"

# Run the test
if __name__ == "__main__":
    pytest.main([__file__])
