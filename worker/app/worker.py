import logging
import sys
from flask import Flask, jsonify
import requests
import mysql.connector
import os
import schedule
import time

app = Flask(__name__)

# Configure the logging format and level
logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# MySQL Database Configuration using environment variables
db_config = {
    'host': os.environ.get('DB_HOST', ''),
    'user': os.environ.get('DB_USER', ''),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', '')
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Function to create the 'data' table if it doesn't exist
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fact LONGTEXT,
            image LONGTEXT
        )
    ''')
    conn.commit()

# Create the 'data' table on application startup
create_table()

@app.route('/')
def index():
    # Retrieve data from the API
    api_data_cat = get_data_from_api_cat()
    api_data_dog = get_data_from_api_dog()

    # Store data in the MySQL database
    store_data_in_database(api_data_cat, api_data_dog)

def get_data_from_api_cat():
    # Replace the URL with the actual API endpoint you want to use
    api_url = 'https://catfact.ninja/fact'
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_data_from_api_dog():
    # Replace the URL with the actual API endpoint you want to use
    api_url = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def store_data_in_database(data_cat, data_dog):
    cursor.execute('INSERT INTO data (fact, image) VALUES (%s, %s)', (data_cat['fact'], data_dog['message']))

    conn.commit()

def job():
    api_data_cat = get_data_from_api_cat()
    api_data_dog = get_data_from_api_dog()
    store_data_in_database(api_data_cat, api_data_dog)

# Schedule the job to run every minute
schedule.every(1).minutes.do(job)

def conn_check():
  try:
    if conn.is_connected():
      print("MySQL Database is alive and connected.")
    else:
      print("Unable to connect to the MySQL Database.")
 
  except Exception as e:
    print(f"Error: {e}")
 
  finally:
    # Close the connection, whether successful or not
    if 'connection' in locals() and conn.is_connected():
        conn.close()
        print("MySQL connection closed.")

schedule.every(15).seconds.do(conn_check)

def test_http_connection():
    try:
        response = requests.get('http://facts')
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        print("Facts frontend is up! Status Code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error: Facts frontend is not responding.")
        print("Exception:", e)

schedule.every(15).seconds.do(test_http_connection)

if __name__ == '__main__':
    # Run the scheduled jobs in a separate thread
    while True:
        schedule.run_pending()
        time.sleep(1) # sleep for 1 second to avoid high CPU usage
