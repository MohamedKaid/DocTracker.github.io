

CREATE TABLE temp_table (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE COLLATE NOCASE,
	dispatch_id INTEGER,
    FOREIGN KEY (dispatch_id) REFERENCES Dispatch(dispatch_id)
);

INSERT INTO New_Drivers (driver_id, name, dispatch_id)
SELECT driver_id, name, dispatch_id FROM Drivers;

DROP TABLE Drivers;

ALTER TABLE New_Drivers RENAME TO Drivers;

-- Command to run script:
-- sqlite3 docTracker.db < update_schema.sql