CREATE TABLE TempHistory(
    tempID INT NOT NULL AUTO_INCREMENT,
    tempC DECIMAL(5,2) NOT NULL,
    tempDate DATE NOT NULL,
    tempTime TIME NOT NULL,
    PRIMARY KEY (tempID)
);