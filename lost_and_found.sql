DROP DATABASE IF EXISTS lost_and_found;
CREATE DATABASE lost_and_found;
USE lost_and_found;


CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('user','admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE categories(
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    expiry_days INT NOT NULL DEFAULT 30,
    CHECK (expiry_days > 0)
);


CREATE TABLE lost_items(
    lost_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(150) NOT NULL,
    date_lost DATE NOT NULL,
    status ENUM('pending','verified','returned') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);


CREATE TABLE found_items(
    found_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(150) NOT NULL,
    date_found DATE NOT NULL,
    expiry_date DATE,
    status ENUM('pending','verified','returned') DEFAULT 'pending',
    admin_action ENUM('archived','sent_to_authority','donated','destroyed'),
    admin_note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (expiry_date IS NULL OR expiry_date >= date_found),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);


CREATE TABLE matches(
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    lost_id INT NOT NULL,
    found_id INT NOT NULL,
    similarity_score DECIMAL(5,2) NOT NULL,
    match_status ENUM('pending','confirmed','rejected') DEFAULT 'pending',
    matched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (similarity_score >= 0 AND similarity_score <= 100),
    FOREIGN KEY (lost_id) REFERENCES lost_items(lost_id),
    FOREIGN KEY (found_id) REFERENCES found_items(found_id)
);




