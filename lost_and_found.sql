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


create table claims (
    claim_id int auto_increment primary key,
    item_type enum('lost','found') not null,
    item_id int not null,
    user_id int not null,
    claim_message text not null,
    status enum('pending','approved','rejected') default 'pending',
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(user_id)
);

create table notifications (
    notification_id int auto_increment primary key,
    user_id int not null,
    message text not null,
    is_read boolean default false,
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(user_id)
);

create table verification_questions (
    question_id int auto_increment primary key,
    found_id int not null,
    question text not null,
    answer text not null,
    created_at datetime default current_timestamp,
    foreign key (found_id) references found_items(found_id)
);