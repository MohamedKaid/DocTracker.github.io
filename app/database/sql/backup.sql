PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE DriverDocs (
    doc_name VARCHAR(50),
    exp_date DATE,
    driver_id INTEGER,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);
INSERT INTO DriverDocs VALUES('Test Card 3','11-22-2023',3);
INSERT INTO DriverDocs VALUES('Test Card 4','11-22-2023',3);
INSERT INTO DriverDocs VALUES('medic','12-08-2023',1);
INSERT INTO DriverDocs VALUES('CDL','01-01-2023',6);
INSERT INTO DriverDocs VALUES('License','01-31-2023',11);
INSERT INTO DriverDocs VALUES('Duck','01-01-2023',20);
INSERT INTO DriverDocs VALUES('Hunt','01-31-2023',20);
INSERT INTO DriverDocs VALUES('Ment','02-02-2024',19);
INSERT INTO DriverDocs VALUES('Way','11-30-2022',19);
INSERT INTO DriverDocs VALUES('Test','11-24-2023',4);
INSERT INTO DriverDocs VALUES('Show','01-01-2023',20);
INSERT INTO DriverDocs VALUES('Down','12-31-2023',20);
CREATE TABLE Dispatch( dispatch_id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50) COLLATE NOCASE, email VARCHAR(100) UNIQUE, pin INTEGER);
INSERT INTO Dispatch VALUES(1,'Mohamed Kaid','mohamedkaid014@gmail.com',1001);
INSERT INTO Dispatch VALUES(2,'Ali','mk.mohamedkaid@gmail.com',1212);
INSERT INTO Dispatch VALUES(3,'ali','alm@gmail.com',1515);
INSERT INTO Dispatch VALUES(4,'ay','ay@gmail.com',1010);
INSERT INTO Dispatch VALUES(5,'al','al@gmail.com',1313);
INSERT INTO Dispatch VALUES(6,NULL,'alim@gmail.com',1313);
INSERT INTO Dispatch VALUES(7,NULL,'alimo@gmail.com',1313);
INSERT INTO Dispatch VALUES(8,NULL,'aim@gmail.com',1212);
INSERT INTO Dispatch VALUES(9,NULL,'ayy@gmail.com',1212);
INSERT INTO Dispatch VALUES(10,NULL,'ayo@gmail.com',1212);
INSERT INTO Dispatch VALUES(11,NULL,'ayo2@gmail.com',1212);
CREATE TABLE Drivers( driver_id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), dispatch_id INTEGER, FOREIGN KEY (dispatch_id) REFERENCES Dispatch(dispatch_id), UNIQUE (name, dispatch_id));
INSERT INTO Drivers VALUES(3,'Mike Ike',2);
INSERT INTO Drivers VALUES(4,'Mike smith',1);
INSERT INTO Drivers VALUES(5,'Khaled Saeed',2);
INSERT INTO Drivers VALUES(6,'A M',3);
INSERT INTO Drivers VALUES(7,'Ali Mohamed',1);
INSERT INTO Drivers VALUES(11,'JACK BOX',3);
INSERT INTO Drivers VALUES(12,'FREE MAN',3);
INSERT INTO Drivers VALUES(13,'MOR GAN',3);
INSERT INTO Drivers VALUES(14,'SAUL GOODMAN',3);
INSERT INTO Drivers VALUES(15,'DRY VER',3);
INSERT INTO Drivers VALUES(17,'GUY BUDDY',3);
INSERT INTO Drivers VALUES(18,'IRON MAN',3);
INSERT INTO Drivers VALUES(19,'MAN O''STEEL',3);
INSERT INTO Drivers VALUES(20,'HARRY HARRINGTON',3);
INSERT INTO Drivers VALUES(21,'GUY FRIEND',3);
INSERT INTO Drivers VALUES(22,'MANBEAR PIG',3);
INSERT INTO Drivers VALUES(23,'Mike sam',1);
INSERT INTO Drivers VALUES(24,'Mike sam',2);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Dispatch',11);
INSERT INTO sqlite_sequence VALUES('Drivers',24);
COMMIT;
