CREATE TABLE TempHistory(
    tempID INT NOT NULL AUTO_INCREMENT,
    tempC FLOAT NOT NULL,
    tempDate DATE NOT NULL,
    tempTime TIME NOT NULL,
    PRIMARY KEY (tempID)
);