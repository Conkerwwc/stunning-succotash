import psycopg2
from psycopg2 import OperationalError, ProgrammingError
import ast # To safely evaluate the string literal read from the file

# Vuyisile Ndlovu (January 21, 2019).
# Working With Files in Python
# https://realpython.com/working-with-files-in-python/

# --- Connection Parameters ---
# Port 5432 is the default for PostgreSQL. Where was the site? Connect (2025). 
# https://dbcode.io/docs/get-started/connect
DB_PARAMS = {
    'dbname': 'postgres', # Use 'postgres' or your specific db
    'user': 'postgres',
    'password': '0451', # <-- CHANGE THIS to your password or my password. Gemini Flash AI (2025). Spend 2 hours here
    # Confused of the Password location it was in Postgres https://database-client.com/
    'host': 'localhost',
    'port': '5432'
}

# --- Database Setup Function ---
def setup_database(conn):
    """A helper function to create tables and insert data."""
    # We use 'ON CONFLICT (id) DO NOTHING' to make this script
    # runnable multiple times without erroring on duplicate keys.
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS departments (
        id SERIAL PRIMARY KEY,
        department_name VARCHAR(100) NOT NULL UNIQUE,  
        department_id INT,
        salary VARCHAR(100), -- Added salary column
        FOREIGN KEY (department_id) REFERENCES departments (id)

    );
    """
    insert_departments_sql = """
    INSERT INTO departments (id, department_name) 
    VALUES (1, 'Data Analysts'), (2, 'Actors'), (3, 'HR')
    ON CONFLICT (id) DO NOTHING;
    """
    insert_employees_sql = """
    INSERT INTO employees (id, name, department_id, salary)
    VALUES 
        (1, 'Jose Perez', 1, '$20000'),       -- Salary will be updated from file
        (2, 'Tech Champion', 2, '$50000'),   -- Salary will be updated from file
        (3, 'Nimish Arvind', 3, '$48000'),   -- Salary will be updated from file
        (4, 'Jennifer Hale', 2, '$73000')    -- Salary will be updated from file
    ON CONFLICT (id) DO NOTHING;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(create_tables_sql)
            cur.execute(insert_departments_sql)
            cur.execute(insert_employees_sql)
        conn.commit()
        print("Database tables created and populated successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error during setup: {e}") # mistakes 89

# --- File I/O and Dictionary Inversion Function ---
def invert_data_from_file(input_filename, output_filename):
    """
    Reads a dictionary from an input file, inverts it,
    and writes the inverted dictionary to an output file.

    Args:
        input_filename (str): The name of the file containing the original dictionary.
        output_filename (str): The name of the file to write the inverted dictionary to.
    
    Returns:
        list: A list of (name, salary) tuples for the database, or None on failure.
    """
    original_dict = {}
    inverted_dict = {}
    employee_data_list = [] # To store (name, salary) tuples for DB

    # File operations demonstrate persistence by reading from permanent storage.
    # DOwney (Pg. 115, 2015).  
    try:
        # Open the file for reading ('r'). The 'with' statement the file is closed.
        # Downey (Pg. 115, 2015). Geeks (2025) 
        # How to open a file using the with statement
        # https://www.geeksforgeeks.org/python/how-to-open-a-file-using-the-with-statement/
        # El (August 12, 2025).
        # USO CORRECTO DEL STATEMENT 'WITH OPEN' EN PYTHON: EJEMPLO DE SINTAXIS
        # https://elblogdelprogramador.com/posts/uso-correcto-del-statement-with-open-en-python-ejemplo-de-sintaxis/#google_vignette

        
        with open(input_filename, 'r') as infile:
            for line in infile:
                line = line.strip() # Remove leading whitespace
                if line and ':' in line: # Ensure line is not empty and has a colon
                    # Split the line into key and value parts at the first colon
                    key_str, value_str = line.split(':', 1)
                    key = key_str.strip()
                    value = value_str.strip()
                    original_dict[key] = value
                    employee_data_list.append((key, value)) # Add (name, salary) tuple
        print(f"Successfully read dictionary from {input_filename}")

    except FileNotFoundError: # Handle file not found error using exception catching.
        # Downey (Pg. 118-119, 2015). 
        print(f"Error: Input file '{input_filename}' not found.")
        return None # Exit the function if the input file doesn't exist 
    except Exception as e: # Catch other potential file reading errors.
        # Downey (Pg. 118-119, 2015).
        print(f"An error occurred while reading '{input_filename}': {e}")
        return None

    # --- Invert the dictionary ---
    # Standard dictionary item iteration and manipulation.
    for key, value in original_dict.items():
        # If the value is already a key in the inverted dictionary, append the original key
        if value in inverted_dict:
            # Ensure the value associated with the inverted key is a list
            if not isinstance(inverted_dict[value], list):
                inverted_dict[value] = [inverted_dict[value]] # Convert to list
            inverted_dict[value].append(key)
            inverted_dict[value].sort() # list of keys sorted alphabetically
        
        else:
            inverted_dict[value] = [key] # Store as a list even for single items for consistency

    # --- Write the inverted dictionary to the output file ---
    # File operations demonstrate persistence by writing to permanent storage.
    # Downey (Pg. 115, 2015).
    try:
        # Open the file in write mode ('w'). Creates the file or overwrites it.
        # Downey (Pg. 115-116, 2015). 
        with open(output_filename, 'w') as outfile:
            outfile.write("{\n") # Start with an opening brace
            items_list = []
            # Sort the inverted dictionary by key (salary) for consistent output
            for value_key in sorted(inverted_dict.keys()):
                original_keys = inverted_dict[value_key]
                # Format the list of original keys as a comma-separated string
                keys_str = ", ".join(sorted(original_keys)) # Keep items sorted
                items_list.append(f"  {value_key}: [{keys_str}]") # Indent items mistake 5

            # The join method combines list elements into a string.
            outfile.write(",\n".join(items_list)) # Join items with commas and newlines
            outfile.write("\n}\n") # closing brace

        print(f"Successfully wrote inverted dictionary to {output_filename}")
        return employee_data_list # Return the data for the database

    except Exception as e: # writing error using exception catching.
        # Downey (Pg. 118-119, 2015).
        print(f"An error occurred while writing to '{output_filename}': {e}")
        return None # Return None on failure. Gemini Flash AI (2025).

# --- Database Insertion Function ---
def insert_employee_data(employee_data_list):
    """ 
    Insert multiple employees and their salaries into the employees table.
    If the employee name already exists, update their salary.
    """
    # This SQL inserts a new row 
    sql = """
    INSERT INTO employees (name, salary) VALUES (%s, %s)
    ON CONFLICT (name) DO UPDATE SET salary = EXCLUDED.salary;
    """
    conn = None
    try:
        # read database configuration params = config()????? WHat's this for anyway, out of my program
    
        # connect to the PostgreSQL database ** this is not the right connection it should be DB
        
        conn = psycopg2.connect(**DB_PARAMS)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT/UPDATE statement for all employees
        cur.executemany(sql, employee_data_list)
        print(f"Successfully inserted/updated {cur.rowcount} employee records in the database.")
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error during data insertion: {error}")
        if conn:
            conn.rollback() # Rollback on error Gemini Flash AI (2025). Got confused here.
    finally:
        if conn is not None:
            conn.close()
            print("Database connection for data insertion closed.")
# To test the insert_vendor() and insert_vendor_list() functions, you use the following code snippet:
# Redrock Postgres (July 31, 2023).
# PostgreSQL Python Tutorial: Insert Data Into a Table https://www.rockdata.net/tutorial/python-insert/


# --- Database Query Function ---
# Geeks (2025). Perform Insert Operations with psycopg2 in Python
# https://www.geeksforgeeks.org/python/perform-insert-operations-with-psycopg2-in-python/
def get_sales_employees():
    """Main function to connect, query, and print results."""
    conn = None # Must define conn outside try for finally to access it
    
    try:
        # ||| Q1. Connect 1.42 MB speed Bad|||
        conn = psycopg2.connect(**DB_PARAMS)
        
        # Note: We run setup_database() in the main block now
        # to ensure tables exist *before* we try to insert data.
        
        # ||| Q2. Create a Cursor |||
        # Using 'with' is a great way to manage cursors
        with conn.cursor() as cur:
            
            # ||| Q3. Use the Query (SELECT, FROM, JOIN, WHERE) |||
            # We use '%s' as a placeholder for our variable.
            # This is the *correct* way to prevent SQL injection (Tech Champion, 2021).
            sql_query = """
            SELECT e.name, d.department_name, e.salary
            FROM employees AS e
            LEFT JOIN departments AS d ON e.department_id = d.id
            WHERE d.department_name = %s;
            """
      
            # The value to pass for the placeholder.
            # Must be in a tuple or list.Spent 4 hours trying to make sense of this. Error 120
            # Geeks (2025). Tuple within a Tuple in Python.
            # https://www.geeksforgeeks.org/python/tuple-within-a-tuple-in-python/
            query_value = ('Actors',) 
            
            # ||| Q4. Run the Query ||| 
            # Psycopg2 9.11 Documentation (2021). Cursor CLass. https://www.psycopg.org/docs/cursor.html
            cur.execute(sql_query, query_value)
            
            # Modified print statement to be accurate
            print(f"\n--- Query Results (Employees in '{query_value[0]}') ---")

            # ||| Q5. Fetch and Display Results |||
            results = cur.fetchall()
            
            if not results:
                print("No employees found in that department.")
            else:
                for row in results:
                    # row[0] Variable is e.name, row[1] is d.department_name, row[2] is e.salary
                    #Geeks (2025). https://www.geeksforgeeks.org/pandas/different-ways-to-iterate-over-rows-in-pandas-dataframe/
                    print(f"Name: {row[0]}, Department: {row[1]}, Salary: {row[2]}")

    except OperationalError as e:
        print(f"CRITICAL: Connection Error. Check credentials/host/port.")
        print(f"Details: {e}")
    except ProgrammingError as e:
        print(f"CRITICAL: SQL Syntax Error.")
        print(f"Details: {e}")
    except (Exception, psycopg2.DatabaseError) as e:
        # Catch any other database errors. Geeks (2025)
        print(f"An unexpected database error occurred: {e}")
        if conn:
            # If an error happens *during* a transaction, roll it back
            conn.rollback() # (Tech Champion, 2021)
    finally:
        # ||| Q6. Cleaning |||
        # This *always* runs to close the connection (Tech Champion, 2021).
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

# ||| Running the main function |||
# This block now controls the entire script flow.
# The __name__ == '__main__' idiom prevents code from running when imported.
# (Downey (Pg.122, 2015). 
if __name__ == "__main__":
    
    # --- Part 1: Database Table ---
    db_conn = None
    try:
        db_conn = psycopg2.connect(**DB_PARAMS)
        setup_database(db_conn)
    except OperationalError as e:
         print(f"CRITICAL: Initial DB Connection Error. Check credentials/host/port.")
         print(f"Details: {e}")
    except (Exception, psycopg2.DatabaseError) as e:
        print(f"An unexpected database error occurred: {e}")
    finally:
        if db_conn:
            db_conn.close()
            print("Database connection for setup closed.\n")

    # --- Part 2: Read file, Write inverted file, and get data for DB ---
    input_file = "salaries.txt"
    output_file = "inverted_salaries.txt"
    # This function now reads the file, writes the inverted file, AND returns the data
    employee_data = invert_data_from_file(input_file, output_file)
    print("") # Newline

    # --- Part 3: Insert/Update data from file into Postgres ---
    if employee_data: # Only run if file processing was successful
        insert_employee_data(employee_data)
    else:
        print("Skipping database insertion due to file reading/writing error.")

    # --- Part 4: Run the original query demo ---
    get_sales_employees()