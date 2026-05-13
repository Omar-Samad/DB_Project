CREATE DATABASE IF NOT EXISTS lost_and_found;
USE lost_and_found;

CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) not null UNIQUE,
    password_hash VARCHAR(255) not null,
    phone VARCHAR(20),
    role ENUM('user','admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories(
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE lost_items(
    lost_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT not null,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(150) not null,
    date_lost DATE NOT NULL,
    status ENUM('pending','verified','returned') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    foreign key (category_id) REFERENCES categories(category_id)
);

CREATE TABLE found_items(
    found_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(150) NOT NULL,
    date_found DATE NOT NULL,
    status ENUM('pending','verified','returned') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    foreign key (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE matches(
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    lost_id INT NOT NULL,
    found_id INT NOT NULL,
    similarity_score DECIMAL(5,2) NOT NULL,
    match_status ENUM('pending','confirmed','rejected') DEFAULT 'pending',
    matched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lost_id) REFERENCES lost_items(lost_id),
    foreign key (found_id) REFERENCES found_items(found_id)
);

use lost_and_found;
ALTER TABLE categories
ADD COLUMN expiry_days INT not null default 30;

ALTER TABLE found_items
add column expiry_date date,
add column admin_action ENUM('archived','sent_to_authority','donated','destroyed'),
add column admin_note text;

