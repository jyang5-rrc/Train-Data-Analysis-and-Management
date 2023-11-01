CREATE DATABASE TrainData;
Go

DROP TABLE Tickets;
DROP TABLE Trips;
DROP TABLE Classes;
DROP TABLE Trains;
DROP TABLE Stations;

DROP TABLE Customers;
DROP TABLE cities;
DROP TABLE States;
DROP TABLE Gender;





Go

CREATE TABLE Genders (
    gender_id INT IDENTITY(1,1),
    gender NVARCHAR(5) NOT NULL,
    CONSTRAINT PK_Genders_GendersID PRIMARY KEY (gender_id),
    CONSTRAINT Gender_UK_Genders UNIQUE (gender)
);
GO

CREATE TABLE States (
    state_id INT IDENTITY(1,1),
    state_name NVARCHAR(35) NOT NULL
    CONSTRAINT PK_States_StateID PRIMARY KEY (state_id),
    CONSTRAINT States_UK_StateName UNIQUE (state_name)
);
Go

CREATE TABLE Cities (
    city_id INT IDENTITY(1,1),
    city_name NVARCHAR(35) NOT NULL,
    state_id INT,
    CONSTRAINT PK_Cities_CityID PRIMARY KEY (city_id),
    CONSTRAINT Fk_Cities_States FOREIGN KEY (state_id) REFERENCES States(state_id)
);

CREATE TABLE Customers (
    cust_id INT,
    first_name NVARCHAR(35) NOT NULL,
    last_name NVARCHAR(35) NOT NULL,
    gender_id INT,
    phone NVARCHAR(20),
    address NVARCHAR(50),
    city_id INT,
    CONSTRAINT PK_Customers_CustID PRIMARY KEY (cust_id),
    CONSTRAINT FK_Customers_Gender FOREIGN KEY (gender_id) REFERENCES Genders(gender_id),
    CONSTRAINT FK_Customers_Cities FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);
Go


CREATE TABLE Stations (
    station_id INT IDENTITY(1,1),
    station_name NVARCHAR(35) NOT NULL,
    CONSTRAINT PK_Stations_StationID PRIMARY KEY (station_id),
    CONSTRAINT Stations_UK_StationName UNIQUE (station_name)
);
Go


CREATE TABLE Trains (
    train_id INT,
    train_name NVARCHAR(20) NOT NULL,
    CONSTRAINT PK_Trains_TrainID PRIMARY KEY (train_id),
    CONSTRAINT Trains_UK_TrainName UNIQUE (train_name)
);
Go


CREATE TABLE Classes (
    class_id INT,
    class_name NVARCHAR(10) NOT NULL,
    CONSTRAINT PK_Classes_ClassID PRIMARY KEY (class_id),
    CONSTRAINT Classes_UK_ClassName UNIQUE (class_name)
);
Go


CREATE TABLE Trips (
    trip_id INT,
    trip_no NVARCHAR(10) NOT NULL,
    station_id_depart INT,
    station_id_arrive INT,
    depart_datetime DATETIME,
    arrive_datetime DATETIME,
    train_id INT,
    class_id INT,
    CONSTRAINT PK_Trips_TripID PRIMARY KEY (trip_id),
    CONSTRAINT Trips_UK_TripNo UNIQUE (trip_no),
    CONSTRAINT FK_Trips_Station_Depart FOREIGN KEY (station_id_depart) REFERENCES Stations(station_id),
    CONSTRAINT FK_Trips_Station_Arrive FOREIGN KEY (station_id_arrive) REFERENCES Stations(station_id),
    CONSTRAINT FK_Trips_Trains FOREIGN KEY (train_id) REFERENCES Trains(train_id),
    CONSTRAINT FK_Trips_Classes FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);
Go


CREATE TABLE Tickets (
    ticket_id INT,
    ticket_no NVARCHAR(10) NOT NULL,
    cust_id INT,
    trip_id INT,
    cost DECIMAL(5, 2) NOT NULL,
    CONSTRAINT PK_Tickets_TicketID PRIMARY KEY (ticket_id),
    CONSTRAINT Tickets_UK_TicketNo UNIQUE (ticket_no),
    CONSTRAINT FK_Tickets_Customers FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
    CONSTRAINT FK_Tickets_Trips FOREIGN KEY (trip_id) REFERENCES Trips(trip_id)
);
Go

