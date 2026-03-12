CREATE TABLE Admin1(
admin_id INT IDENTITY(1,1) PRIMARY KEY,
username VARCHAR(50),
password VARCHAR(50)
);

INSERT INTO Admin1(username,password)
VALUES('admin','admin123');

CREATE TABLE Rooms1(
room_id INT IDENTITY(1,1) PRIMARY KEY,
room_name VARCHAR(50),
capacity INT
);

CREATE TABLE Students2(
student_id INT PRIMARY KEY,
name VARCHAR(100),
department VARCHAR(50),
room_id INT,
FOREIGN KEY (room_id) REFERENCES Rooms1(room_id)
);


CREATE TABLE Seating1(
student_id INT PRIMARY KEY,
room_id INT,
seat_number INT,
FOREIGN KEY (student_id) REFERENCES Students2(student_id),
FOREIGN KEY (room_id) REFERENCES Rooms1(room_id)
);



SELECT * FROM Admin1;
SELECT * FROM Rooms1;
SELECT * FROM Students2;
SELECT * FROM Seating1;
