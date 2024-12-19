from flask import Flask, render_template
import mysql.connector
import random
import os

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': os.environ.get('DB_HOST', ''),
    'user': os.environ.get('DB_USER', ''),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', '')
}

# Function to get a random record from the database
def get_random_record():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM data ORDER BY RAND() LIMIT 1')
    record = cursor.fetchone()

    cursor.close()
    conn.close()

    return record

# Define route to display random text and image
@app.route('/')
def index():
    # Fetch random record from the database
    record = get_random_record()

    # Render the template with the data
    return render_template('index.html', text=record['fact'], image_url=record['image'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
