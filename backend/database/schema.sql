DROP DATABASE hotel;
CREATE DATABASE hotel;

-- Drop the database if it exists to start fresh
DROP DATABASE IF EXISTS hotel;

-- Create the database
CREATE DATABASE hotel;

-- Select the database to use
USE hotel;

-- Create the users table with a secure password hash length
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) DEFAULT NULL,
    email VARCHAR(50) DEFAULT NULL,
    hash_password VARCHAR(255) NOT NULL,
    user_type ENUM('user','manager') NOT NULL
);

CREATE TABLE rooms (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- NEW COLUMN ADDED FOR 3-DIGIT NUMBER
    room_number INT DEFAULT NULL,
    room_type VARCHAR(50) DEFAULT NULL,
    price DECIMAL(10,2) DEFAULT NULL,
    available TINYINT(1) DEFAULT 1
);

CREATE TABLE bookings (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    check_out DATE NOT NULL,
    check_in DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

CREATE TABLE reservations (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    booking_id INT DEFAULT NULL,
    status VARCHAR(10) DEFAULT NULL,
    confirmation_number VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

CREATE TABLE payments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    booking_id INT DEFAULT NULL,
    amount DECIMAL(10,2) DEFAULT NULL,
    method VARCHAR(12) DEFAULT NULL,
    cvv INT DEFAULT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- UPDATED INSERT statements with new room numbers
INSERT INTO rooms (room_number, room_type, price, available) VALUES
-- Floor 1: Standard Rooms
(101, 'Standard Room', 120.00, 1), (102, 'Standard Room', 120.00, 1),
(103, 'Standard Room', 120.00, 1), (104, 'Standard Room', 120.00, 1),
(105, 'Standard Room', 120.00, 1), (106, 'Standard Room', 120.00, 1),
(107, 'Standard Room', 120.00, 1), (108, 'Standard Room', 120.00, 1),
(109, 'Standard Room', 120.00, 1), (110, 'Standard Room', 120.00, 1),
-- Floor 2: Deluxe Rooms
(201, 'Deluxe Room', 175.00, 1), (202, 'Deluxe Room', 175.00, 1),
(203, 'Deluxe Room', 175.00, 1), (204, 'Deluxe Room', 175.00, 1),
(205, 'Deluxe Room', 175.00, 1), (206, 'Deluxe Room', 175.00, 1),
(207, 'Deluxe Room', 175.00, 1), (208, 'Deluxe Room', 175.00, 1),
(209, 'Deluxe Room', 175.00, 1), (210, 'Deluxe Room', 175.00, 1),
-- Floor 3: Suite Rooms
(301, 'Suite Room', 250.00, 1), (302, 'Suite Room', 250.00, 1),
(303, 'Suite Room', 250.00, 1), (304, 'Suite Room', 250.00, 1),
(305, 'Suite Room', 250.00, 1), (306, 'Suite Room', 250.00, 1),
(307, 'Suite Room', 250.00, 1), (308, 'Suite Room', 250.00, 1),
(309, 'Suite Room', 250.00, 1), (310, 'Suite Room', 250.00, 1);