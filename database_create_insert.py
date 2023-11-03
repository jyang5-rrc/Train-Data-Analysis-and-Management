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
                "Genders": """
                            CREATE TABLE Genders (
                                gender_id INT IDENTITY(1,1),
                                gender NVARCHAR(5) NOT NULL,
                                CONSTRAINT PK_Genders_GendersID PRIMARY KEY (gender_id),
                                CONSTRAINT Gender_UK_Genders UNIQUE (gender)
                            );
                            """,
                "States": """
                            CREATE TABLE States (
                                state_id INT IDENTITY(1,1),
                                state_name NVARCHAR(35) NOT NULL
                                CONSTRAINT PK_States_StateID PRIMARY KEY (state_id),
                                CONSTRAINT States_UK_StateName UNIQUE (state_name)
                            );
                            """,
                "Cities": """
                            CREATE TABLE Cities (
                                city_id INT IDENTITY(1,1),
                                city_name NVARCHAR(35) NOT NULL,
                                state_id INT,
                                CONSTRAINT PK_Cities_CityID PRIMARY KEY (city_id),
                                CONSTRAINT Fk_Cities_States FOREIGN KEY (state_id) REFERENCES States(state_id)
                            );
                            """,
                "Customers": """
                            CREATE TABLE Customers (
                                cust_id INT,
                                first_name NVARCHAR(35) NOT NULL,
                                last_name NVARCHAR(35) NOT NULL,
                                gender_id INT,
                                phone NVARCHAR(20),
                                address NVARCHAR(50),
                                city_id INT,
                                CONSTRAINT PK_Customers_CustID PRIMARY KEY (cust_id),
                                CONSTRAINT FK_Customers_Genders FOREIGN KEY (gender_id) REFERENCES Genders(gender_id),
                                CONSTRAINT FK_Customers_Cities FOREIGN KEY (city_id) REFERENCES Cities(city_id)
                            );
                            """,
                "Classes": """
                            CREATE TABLE Classes (
                                class_id INT,
                                class_name NVARCHAR(10) NOT NULL,
                                CONSTRAINT PK_Classes_ClassID PRIMARY KEY (class_id),
                                CONSTRAINT Classes_UK_ClassName UNIQUE (class_name)
                            );
                            """,
                "Trains": """
                            CREATE TABLE Trains (
                                train_id INT,
                                train_name NVARCHAR(20) NOT NULL,
                                CONSTRAINT PK_Trains_TrainID PRIMARY KEY (train_id),
                                CONSTRAINT Trains_UK_TrainName UNIQUE (train_name)
                            );
                          """,
                "Stations": """
                            CREATE TABLE Stations (
                                station_id INT IDENTITY(1,1),
                                station_name NVARCHAR(35) NOT NULL,
                                CONSTRAINT PK_Stations_StationID PRIMARY KEY (station_id),
                                CONSTRAINT Stations_UK_StationName UNIQUE (station_name)
                            );
                            """,
                "Trips": """ 
                            CREATE TABLE Trips (
                                trip_id INT,
                                trip_no NVARCHAR(10) NOT NULL,
                                station_id_depart INT,
                                station_id_arrive INT,
                                depart_datetime DATETIME,
                                arrive_datetime DATETIME,
                                cost DECIMAL(5, 2) NOT NULL,
                                train_id INT,
                                CONSTRAINT PK_Trips_TripID PRIMARY KEY (trip_id),
                                CONSTRAINT Trips_UK_TripNo UNIQUE (trip_no),
                                CONSTRAINT FK_Trips_Station_Depart FOREIGN KEY (station_id_depart) REFERENCES Stations(station_id),
                                CONSTRAINT FK_Trips_Station_Arrive FOREIGN KEY (station_id_arrive) REFERENCES Stations(station_id),
                                CONSTRAINT FK_Trips_Trains FOREIGN KEY (train_id) REFERENCES Trains(train_id),
                            );
                            """,
                "Tickets": """
                            CREATE TABLE Tickets (
                                ticket_id INT,
                                ticket_no NVARCHAR(10) NOT NULL,
                                cust_id INT,
                                trip_id INT,
                                class_id INT,
                                cost DECIMAL(5, 2) NOT NULL,
                                comfirm_ticket CHAR(1),
                                CONSTRAINT PK_Tickets_TicketID PRIMARY KEY (ticket_id),
                                CONSTRAINT Tickets_UK_TicketNo UNIQUE (ticket_no),
                                CONSTRAINT FK_Tickets_Customers FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
                                CONSTRAINT FK_Tickets_Trips FOREIGN KEY (trip_id) REFERENCES Trips(trip_id),
                                CONSTRAINT FK_Tickets_Classes FOREIGN KEY (class_id) REFERENCES Classes(class_id)
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
        IF NOT EXISTS (SELECT * FROM Genders WHERE gender = ?)
            INSERT INTO Genders (gender) VALUES (?)
        """, (gender, gender))

        
     # Insert into Cities table, avoiding duplicates
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
        cursor.execute("SELECT gender_id FROM Genders WHERE gender = ?", row.gender)
        gender_id = cursor.fetchone()[0]
        
        # Fetch state_id for the customer
        cursor.execute("SELECT state_id FROM States WHERE state_name = ?", row.state)
        state_id = cursor.fetchone()[0]
        
        # Insert cities data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Cities WHERE city_name = ? AND state_id = ?)
            INSERT INTO Cities (city_name, state_id)
            VALUES (?, ?)
        """, (row.city, state_id, row.city, state_id))
        
        # Fetch city_id for the customer
        cursor.execute("SELECT city_id FROM Cities WHERE city_name = ?", row.city)
        city_id = cursor.fetchone()[0]
        
        # Insert customer data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Customers WHERE cust_id = ?)
            INSERT INTO Customers (cust_id, first_name, last_name, gender_id, phone, address, city_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row.cust_id, row.cust_id, row.first_name, row.last_name, gender_id, row.phone, row.address, city_id))


        # Fetch station_id for the Trips table
        cursor.execute("SELECT station_id FROM Stations WHERE station_name = ?", row.station_id_depart)
        station_id_depart = cursor.fetchone()[0]
        
        # Fetch station_id for the Trips table
        cursor.execute("SELECT station_id FROM Stations WHERE station_name = ?", row.station_id_arrive)
        station_id_arrive = cursor.fetchone()[0]
        
        # Insert trips data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Trips WHERE trip_id = ?)
            INSERT INTO Trips (trip_id, trip_no, station_id_depart, station_id_arrive, depart_datetime, arrive_datetime,cost, train_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (row.trip_id, row.trip_id, row.trip_no, station_id_depart, station_id_arrive, row.depart_datetime, row.arrive_datetime, row.cost, row.train_id))

        # Insert tickets data
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Tickets WHERE ticket_id = ?)
            INSERT INTO Tickets (ticket_id, ticket_no, cust_id, trip_id, class_id, cost)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (row.ticket_id, row.ticket_id, row.ticket_no, row.cust_id, row.trip_id, row.class_id, row.cost))

    conn.commit()
    print("Data inserted successfully!")

    

# Create tables and insert data
create_tables() 
csv_file_path = 'TrainData.csv'
insert_data_from_csv(csv_file_path)

# Clean up
cursor.close()
conn.close()
