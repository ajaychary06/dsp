import pymysql
import random

# Database connection details
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "secure_db"

# Function to create the database if it doesn't exist
def create_database():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    connection.commit()
    connection.close()
    print(f"Database '{db_name}' created or already exists.")

# Function to create tables and insert random data
def setup_database():
    # Ensure the database is created before connecting to it
    create_database()
    
    db = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        group_name ENUM('H', 'R') NOT NULL
    );
    """)

    # Create healthcare table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS healthcare (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        gender BOOLEAN,
        age INT,
        weight FLOAT,
        height FLOAT,
        health_history TEXT
    );
    """)

    # Generate random data
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
    last_names = ["Smith", "Doe", "Brown", "Johnson", "Williams", "Jones", "Davis", "Miller", "Wilson", "Taylor"]
    health_issues = ["No major issues", "Asthma", "Diabetes", "Hypertension", "Allergies", "Heart disease", "Arthritis"]
    
    for _ in range(100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        gender = random.choice([0, 1])  # 0 for female, 1 for male
        age = random.randint(18, 80)
        weight = round(random.uniform(50, 100), 1)
        height = round(random.uniform(150, 200), 1)
        health_history = random.choice(health_issues)

        cursor.execute("""
        INSERT INTO healthcare (first_name, last_name, gender, age, weight, height, health_history)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, gender, age, weight, height, health_history))

    db.commit()
    db.close()
    print("Database setup complete with 100 random records.")

if __name__ == "__main__":
    setup_database()
