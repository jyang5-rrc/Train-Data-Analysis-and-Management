import pandas as pd
import pyodbc
import os

#os.chdir(r'C:\Users\jocel\Desktop\Term3\DB2\introductory project\TrainData--wroking on')

# Database connection parameters - replace with your actual credentials
server = 'JOCELYN'
username = 'sa'
password = 'wojiushiyjj522'
driver = '{ODBC Driver 17 for SQL Server}'  # Adjust your SQL Server ODBC driver as needed

# Connect to the server (without specifying the database)
conn_str = f'DRIVER={driver};SERVER={server};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

# Create the database if it doesn't exist
db_name = 'TrainData'
cursor.execute(f"IF DB_ID(N'{db_name}') IS NULL CREATE DATABASE [{db_name}];")

# Close the initial connection to reconnect with the new database
cursor.close()
conn.close()

# Connect to the newly created database
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={db_name};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Rest of your script for table creation and data insertion
# ...

# Example for how to create tables and insert data
def create_tables():
    # Drop tables if they exist to avoid errors on re-creation
    tables = {
                "Gender": """
                            CREATE TABLE Gender (
                                gender_id INT PRIMARY KEY IDENTITY(1,1),
                                gender NVARCHAR(10) NOT NULL
                            );
                            """,
                "States": """
                            CREATE TABLE States (
                                state_id INT PRIMARY KEY IDENTITY(1,1),
                                state_name NVARCHAR(100) NOT NULL
                            );
                            """,
                "Customers": """
                            CREATE TABLE Customers (
                                cust_id INT PRIMARY KEY,
                                first_name NVARCHAR(100) NOT NULL,
                                last_name NVARCHAR(100) NOT NULL,
                                gender_id INT,
                                phone NVARCHAR(20),
                                address NVARCHAR(255),
                                city NVARCHAR(100),
                                state_id INT,
                                date_created DATETIME,
                                customerAge INT,
                                CONSTRAINT fk_Customers_Gender FOREIGN KEY (gender_id) REFERENCES Gender(gender_id),
                                CONSTRAINT fk_Customers_States FOREIGN KEY (state_id) REFERENCES States(state_id)
                            );
                            """,
                "Classes": """
                            CREATE TABLE Classes (
                                class_id INT PRIMARY KEY,
                                class_name NVARCHAR(50) NOT NULL
                            );
                            """,
                "Trains": """
                            CREATE TABLE Trains (
                                train_id INT PRIMARY KEY,
                                train_name NVARCHAR(100) NOT NULL,
                            );
                          """,
                "Stations": """
                            CREATE TABLE Stations (
                                station_id INT PRIMARY KEY IDENTITY(1,1),
                                station_name NVARCHAR(255) NOT NULL,
                            );
                            """,
                "Trips": """ 
                            CREATE TABLE Trips (
                                trip_id INT PRIMARY KEY,
                                trip_no NVARCHAR(50) NOT NULL,
                                depart_datetime DATETIME,
                                station_id_depart INT,
                                arrive_datetime DATETIME,
                                station_id_arrive INT,
                                CONSTRAINT fk_Trips_Station_Depart FOREIGN KEY (station_id_depart) REFERENCES Stations(station_id),
                                CONSTRAINT fk_Trips_Station_Arrive FOREIGN KEY (station_id_arrive) REFERENCES Stations(station_id)
                            );
                            """,
                "Tickets": """
                            CREATE TABLE Tickets (
                                ticket_id INT PRIMARY KEY,
                                ticket_no NVARCHAR(50) NOT NULL,
                                cost DECIMAL(10, 2) NOT NULL,
                                trip_id INT,
                                cust_id INT,
                                train_id INT,
                                class_id INT,
                                CONSTRAINT fk_Tickets_Trip FOREIGN KEY (trip_id) REFERENCES Trips(trip_id),
                                CONSTRAINT fk_Tickets_Customer FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
                                CONSTRAINT fk_Tickets_Trains FOREIGN KEY (train_id) REFERENCES Trains(train_id),
                                CONSTRAINT fk_Tickets_Classes FOREIGN KEY (class_id) REFERENCES Classes(class_id)
                            );
                            """
            }
    
    for table, create_sql in tables.items(): #.items() means to get the key and value of the dictionary,otherwise it will only get the key
        cursor.execute(f"IF OBJECT_ID('{table}', 'U') IS NOT NULL DROP TABLE {table};")

        # Create tables
        cursor.execute(create_sql)
        
    conn.commit()

def insert_data_from_csv(file_path):
    data = pd.read_csv(file_path)

    # Insert into Gender table, avoiding duplicates
    for gender in data['gender'].drop_duplicates():
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Gender WHERE gender = ?)
            INSERT INTO Gender (gender) VALUES (?)
        """, (gender, gender))
    
    # Insert into States table, avoiding duplicates
    for state in data['state'].drop_duplicates():
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM States WHERE state_name = ?)
            INSERT INTO States (state_name) VALUES (?)
        """, (state, state))

    # Insert into Stations, Trains, and Classes tables
    for station_name in data['station_id_depart'].drop_duplicates():
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Stations WHERE station_name= ?)
            INSERT INTO Stations (station_name) VALUES (?)
        """, (station_name, station_name))
        
    for station_name in data['station_id_arrive'].drop_duplicates():
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Stations WHERE station_name = ?)
            INSERT INTO Stations (station_name) VALUES (?)
        """, (station_name, station_name))
    
    for train_id, train_name in data[['train_id', 'train_name']].drop_duplicates().itertuples(index=False):
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Trains WHERE train_id = ?)
            INSERT INTO Trains (train_id, train_name) VALUES (?, ?)
        """, (train_id, train_id, train_name))

    for class_id, class_name in data[['class_id', 'class_name']].drop_duplicates().itertuples(index=False):
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Classes WHERE class_id = ?)
            INSERT INTO Classes (class_id, class_name) VALUES (?, ?)
        """, (class_id, class_id, class_name))

    # Insert into Customer, Trip, and Ticket tables
    # Assuming cust_id, trip_id, and ticket_id are unique in the dataset
    for row in data.itertuples():
        # Fetch gender_id for the customer
        cursor.execute("SELECT gender_id FROM Gender WHERE gender = ?", row.gender)
        gender_id = cursor.fetchone()[0]
        
        # Fetch state_id for the customer
        cursor.execute("SELECT state_id FROM States WHERE state_name = ?", row.state)
        state_id = cursor.fetchone()[0]
        
        # Insert customer data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Customers WHERE cust_id = ?)
            INSERT INTO Customers (cust_id, first_name, last_name, gender_id, phone, address, city, state_id, date_created, customerAge)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (row.cust_id, row.cust_id, row.first_name, row.last_name, gender_id, row.phone, row.address, row.city, state_id, row.date_created, row.CustomerAge))


        # Fetch station_id for the Trips table
        cursor.execute("SELECT station_id FROM Stations WHERE station_name = ?", row.station_id_depart)
        station_id_depart = cursor.fetchone()[0]
        
        # Fetch station_id for the Trips table
        cursor.execute("SELECT station_id FROM Stations WHERE station_name = ?", row.station_id_arrive)
        station_id_arrive = cursor.fetchone()[0]
        
        # Insert trips data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Trips WHERE trip_id = ?)
            INSERT INTO Trips (trip_id, trip_no, depart_datetime, station_id_depart, arrive_datetime, station_id_arrive)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (row.trip_id, row.trip_id, row.trip_no, row.depart_datetime, station_id_depart, row.arrive_datetime, station_id_arrive))

        # Insert tickets data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Tickets WHERE ticket_id = ?)
            INSERT INTO Tickets (ticket_id, ticket_no, cost, trip_id, cust_id, train_id, class_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row.ticket_id, row.ticket_id, row.ticket_no, row.cost, row.trip_id, row.cust_id, row.train_id, row.class_id))

    conn.commit()

    

# Create tables and insert data
create_tables()
csv_file_path = 'TrainData.csv'
insert_data_from_csv(csv_file_path)

# Clean up
cursor.close()
conn.close()
