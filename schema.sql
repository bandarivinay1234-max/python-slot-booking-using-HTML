-- Slot Booking Database Schema
-- Run this script in MySQL to set up the database

CREATE DATABASE IF NOT EXISTS slot_booking;
USE slot_booking;

-- Slots table
CREATE TABLE IF NOT EXISTS slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_booked TINYINT(1) DEFAULT 0,
    booked_by VARCHAR(100) DEFAULT NULL,
    booked_email VARCHAR(150) DEFAULT NULL,
    booked_at DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed sample slots: 9 AM – 5 PM in 1-hour blocks for the next 3 days
-- Day 1
INSERT INTO slots (slot_date, start_time, end_time) VALUES
(CURDATE(), '09:00:00', '10:00:00'),
(CURDATE(), '10:00:00', '11:00:00'),
(CURDATE(), '11:00:00', '12:00:00'),
(CURDATE(), '12:00:00', '13:00:00'),
(CURDATE(), '13:00:00', '14:00:00'),
(CURDATE(), '14:00:00', '15:00:00'),
(CURDATE(), '15:00:00', '16:00:00'),
(CURDATE(), '16:00:00', '17:00:00');

-- Day 2
INSERT INTO slots (slot_date, start_time, end_time) VALUES
(CURDATE() + INTERVAL 1 DAY, '09:00:00', '10:00:00'),
(CURDATE() + INTERVAL 1 DAY, '10:00:00', '11:00:00'),
(CURDATE() + INTERVAL 1 DAY, '11:00:00', '12:00:00'),
(CURDATE() + INTERVAL 1 DAY, '12:00:00', '13:00:00'),
(CURDATE() + INTERVAL 1 DAY, '13:00:00', '14:00:00'),
(CURDATE() + INTERVAL 1 DAY, '14:00:00', '15:00:00'),
(CURDATE() + INTERVAL 1 DAY, '15:00:00', '16:00:00'),
(CURDATE() + INTERVAL 1 DAY, '16:00:00', '17:00:00');

-- Day 3
INSERT INTO slots (slot_date, start_time, end_time) VALUES
(CURDATE() + INTERVAL 2 DAY, '09:00:00', '10:00:00'),
(CURDATE() + INTERVAL 2 DAY, '10:00:00', '11:00:00'),
(CURDATE() + INTERVAL 2 DAY, '11:00:00', '12:00:00'),
(CURDATE() + INTERVAL 2 DAY, '12:00:00', '13:00:00'),
(CURDATE() + INTERVAL 2 DAY, '13:00:00', '14:00:00'),
(CURDATE() + INTERVAL 2 DAY, '14:00:00', '15:00:00'),
(CURDATE() + INTERVAL 2 DAY, '15:00:00', '16:00:00'),
(CURDATE() + INTERVAL 2 DAY, '16:00:00', '17:00:00');
