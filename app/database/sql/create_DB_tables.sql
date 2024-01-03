BEGIN;
CREATE TABLE Dispatch (
    dispatch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) COLLATE NOCASE,
    email VARCHAR(100) UNIQUE,
    pin INTEGER
);

CREATE TABLE Drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) COLLATE NOCASE,
	dispatch_id INTEGER,
    FOREIGN KEY (dispatch_id) REFERENCES Dispatch(dispatch_id)
);

CREATE TABLE DriverDocs (
    doc_name VARCHAR(50),
    exp_date DATE,
    driver_id INTEGER,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);
COMMIT;