USE lost_and_found;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/lost_items.csv'
INTO TABLE lost_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
ALTER TABLE found_items 
MODIFY COLUMN status ENUM('pending','verified','expired','returned') DEFAULT 'pending';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/found_items.csv'
INTO TABLE found_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(found_id, user_id, category_id, item_name, description, 
 location, date_found, expiry_date, status, 
 @admin_action, @admin_note, created_at)
SET 
    admin_action = NULLIF(@admin_action, ''),
    admin_note   = NULLIF(@admin_note, '');




LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/matches.csv'
INTO TABLE matches
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

select * from users;
update users
set full_name='Awais Khan'
where user_id =4;

DELETE FROM matches
where match_status='rejected'
limit 1;


SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM lost_items;
SELECT COUNT(*) FROM found_items;
SELECT COUNT(*) FROM matches;

SELECT COUNT(*) FROM users WHERE email IS NULL;
SELECT COUNT(*) FROM users WHERE full_name IS NULL;
SELECT COUNT(*) FROM lost_items WHERE location IS NULL;
SELECT COUNT(*) FROM lost_items WHERE item_name IS NULL;
SELECT COUNT(*) FROM found_items WHERE expiry_date IS NULL;
SELECT COUNT(*) FROM matches WHERE similarity_score IS NULL;


SELECT COUNT(*) FROM lost_items l JOIN users u ON l.user_id = u.user_id;
SELECT COUNT(*) FROM found_items f JOIN users u ON f.user_id = u.user_id;
SELECT COUNT(*) FROM lost_items l JOIN categories c ON l.category_id = c.category_id;
SELECT COUNT(*) FROM found_items f JOIN categories c ON f.category_id = c.category_id;
SELECT COUNT(*) FROM matches m JOIN lost_items l ON m.lost_id = l.lost_id JOIN found_items f ON m.found_id = f.found_id;