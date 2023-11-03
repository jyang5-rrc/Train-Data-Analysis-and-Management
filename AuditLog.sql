DROP TABLE IF EXISTS customersAuditLog;
GO

CREATE TABLE customersAuditLog (
    customerAuditID INT IDENTITY(1,1),
    modifiedBy NVARCHAR(20),
    modifiedDate DATETIME,
    operationType NVARCHAR(6),
    cust_id INT,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    CONSTRAINT PK_customersAuditLog PRIMARY KEY (customerAuditID),
    --CONSTRAINT FK_customersAuditLog_Customers FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);
GO

DROP TRIGGER IF EXISTS trg_customers_audit;
GO

CREATE TRIGGER trg_customers_audit 
ON customers
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Handle inserted or updated rows
    IF EXISTS (SELECT * FROM inserted)
    BEGIN
        -- Handle the case for updates
        IF EXISTS (SELECT * FROM deleted)
        BEGIN
            INSERT INTO customersAuditLog (modifiedBy, modifiedDate, operationType, cust_id, first_name, last_name)
            SELECT SUSER_SNAME(), GETDATE(), 'UPDATE', i.cust_id, i.first_name, i.last_name
            FROM inserted i;
        END
        ELSE -- Handle pure inserts
        BEGIN
            INSERT INTO customersAuditLog (modifiedBy, modifiedDate, operationType, cust_id, first_name, last_name)
            SELECT SUSER_SNAME(), GETDATE(), 'INSERT', i.cust_id, i.first_name, i.last_name
            FROM inserted i;
        END
    END

    -- Handle deleted rows
    IF EXISTS (SELECT * FROM deleted) AND NOT EXISTS (SELECT * FROM inserted)
    BEGIN
        INSERT INTO customersAuditLog (modifiedBy, modifiedDate, operationType, cust_id, first_name, last_name)
        SELECT SUSER_SNAME(), GETDATE(), 'DELETE', d.cust_id, d.first_name, d.last_name
        FROM deleted d;
    END
END
GO

DELETE FROM Customers WHERE cust_id IN (1025, 1026, 1027, 1028);
GO 

INSERT INTO customers (cust_id, first_name, last_name)
VALUES ('1025', 'Jen', 'Irving');
GO

INSERT INTO customers (cust_id, first_name, last_name)
VALUES ('1026', 'Gene', 'Simons');
GO

INSERT INTO customers (cust_id, first_name, last_name)
VALUES ('1027', 'Sidney', 'Mark');
GO

INSERT INTO customers (cust_id, first_name, last_name)
VALUES ('1028', 'Prescot', 'Mandy');
GO


UPDATE customers
SET first_name = 'Chris', last_name = 'Irving'
WHERE first_name = 'Jen' AND last_name = 'Irving';
GO

DELETE FROM customers
WHERE first_name = 'Prescot' AND last_name = 'Mandy';
GO