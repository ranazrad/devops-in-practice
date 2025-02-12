CREATE DATABASE IF NOT EXISTS music;
USE music;

CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL
);

INSERT INTO songs (title, artist) VALUES 
('Shape of You', 'Ed Sheeran'),
('Blinding Lights', 'The Weeknd'),
('Bohemian Rhapsody', 'Queen');
