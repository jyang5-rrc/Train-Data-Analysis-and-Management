CREATE PROCEDURE time_corrector
AS
BEGIN
    SET NOCOUNT ON; -- NOCOUNT is used to prevent the extra messages (like "1 row affected") from being returned to the client.
    BEGIN TRY 
        BEGIN TRANSACTION;

        DECLARE @MixupRows INT;
        
        UPDATE Trips -- role is to update the trip_id column in the Trips table 
        SET
            --depart_datetime = arrive_datetime,
            --arrive_datetime = depart_datetime
        WHERE DATEDIFF(MINUTE, depart_datetime, arrive_datetime) < 0; -- DATEIFF() is used to compare the two dates and return the difference in days
    
        SET @MixupRows = @@ROWCOUNT; -- @@ROWCOUNT is used to return the number of rows affected by the last statement

        COMMIT TRANSACTION;

        PRINT CAST(@MixupRows AS NVARCHAR(10)) + ' Rows are swapped/updated.';
        PRINT 'Completion time: ' + CONVERT(NVARCHAR(30), GETDATE(), 121); 

    END TRY

    BEGIN CATCH
        ROLLBACK TRANSACTION; -- ROLLBACK is used to undo the changes made by the transaction
        PRINT 'Error: ' + ERROR_MESSAGE();
    END CATCH;

END;
GO


--version 2
CREATE PROCEDURE time_corrector
AS
BEGIN
    SET NOCOUNT ON; -- NOCOUNT is used to prevent the extra messages (like "1 row affected") from being returned to the client.
    BEGIN TRY 
        BEGIN TRANSACTION;

        DECLARE @MixupRows INT;
        
        SELECT @MixupRows = COUNT(*) 
        FROM Trips 
        WHERE DATEDIFF(MINUTE, depart_datetime, arrive_datetime) < 0; -- DATEDIFF() is used to compare the two dates and return the difference in days
        
        COMMIT TRANSACTION;

        PRINT CAST(@MixupRows AS NVARCHAR(10)) + ' Rows will be swapped/updated.';
        PRINT 'Completion time: ' + CONVERT(NVARCHAR(30), GETDATE(), 121); 

    END TRY

    BEGIN CATCH
        ROLLBACK TRANSACTION; -- ROLLBACK is used to undo the changes made by the transaction
        PRINT 'Error: ' + ERROR_MESSAGE();
    END CATCH;

END
GO
