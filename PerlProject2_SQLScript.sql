CREATE DATABASE users;
USE users;
CREATE TABLE users (
	user_id int NOT NULL AUTO_INCREMENT,
	username varchar(50) NOT NULL UNIQUE,
    password varchar(50) NOT NULL,
    PRIMARY KEY(user_id)
);
INSERT INTO users (username, password)
	VALUES ('johndoe', '!123a');
INSERT INTO users (username, password)
	VALUES ('janedoe', 'Abc12');
INSERT INTO users (username, password)
	VALUES ('johnny_cash', 'blabla55');
SELECT * FROM users;
CREATE TABLE participants (
	participant_id int NOT NULL AUTO_INCREMENT,
	age int NOT NULL,
    gender varchar(10),
    address varchar(50),
    date_time datetime,
    user_id int,
    PRIMARY KEY (participant_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
SELECT * FROM participants;