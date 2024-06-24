import requests
import json
import sqlite3
import os

# Function to get exoplanet data from NASA API
def get_exoplanet_data():
    url = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI'
    params = {
        'table': 'exoplanet',
        'format': 'json'
    }
    response = requests.get(url, params=params)

    # Print response for debugging
    print("Response status code:", response.status_code)
    print("Response text:", response.text[:500])  # Print first 500 characters of response text

    return response

# Function to get the status code of the response
def get_status_code(response):
    return response.status_code

# Function to save JSON data to a file
def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to create SQLite database and exoplanets table
def create_database_and_table():
    try:
        conn = sqlite3.connect('exoplanets.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS exoplanets
                     (name TEXT, discovery_method TEXT, orbital_period REAL, radius REAL)''')
        conn.commit()
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

# Function to store information in the exoplanets table
def store_in_db(exoplanets):
    conn = sqlite3.connect('exoplanets.db')
    c = conn.cursor()
    try:
        for exoplanet in exoplanets:
            c.execute("INSERT INTO exoplanets (name, discovery_method, orbital_period, radius) VALUES (?, ?, ?, ?)",
                      (exoplanet.get('pl_name'), exoplanet.get('pl_discmethod'), exoplanet.get('pl_orbper'),
                       exoplanet.get('pl_rade')))
        conn.commit()
        print("Exoplanet data has been successfully stored in the database.")
    except sqlite3.Error as e:
        print(f"Error storing data: {e}")
    finally:
        conn.close()

# Function to parse and print interesting exoplanet data
def print_exoplanet_data(exoplanets):
    for exoplanet in exoplanets[:5]:  # Print data for first 5 exoplanets
        print(f"Name: {exoplanet.get('pl_name')}")
        print(f"Discovery Method: {exoplanet.get('pl_discmethod')}")
        print(f"Orbital Period: {exoplanet.get('pl_orbper')}")
        print(f"Radius: {exoplanet.get('pl_rade')}")
        print()

# Main function
def main():
    response = get_exoplanet_data()

    if get_status_code(response) == 200:
        try:
            exoplanet_data = response.json()
            save_json_to_file(exoplanet_data, 'exoplanets.json')
            create_database_and_table()  # Ensure database and table exist
            store_in_db(exoplanet_data)
            print("Interesting Exoplanet Data:")
            print_exoplanet_data(exoplanet_data)
        except json.JSONDecodeError as je:
            print(f"Error decoding JSON response: {je}")
    else:
        print(f"Failed to retrieve exoplanet information. Status code: {get_status_code(response)}")

if __name__ == '__main__':
    main()
