-- Create the database
CREATE DATABASE IF NOT EXISTS boulanger_scraping;

-- Use the database
USE boulanger_scraping;

-- Create the table to store product information
CREATE TABLE IF NOT EXISTS produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produit VARCHAR(255) NOT NULL,
    note VARCHAR(10),
    avis VARCHAR(50)
);
