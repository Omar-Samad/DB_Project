Milestone 3 — Dataset Preprocessing
Data Flow:
Prepared the whole data using Python and Faker. 5 csv files were created.
Data enters the system through 3 points.
1.	When users enter the system for the first time, they register themselves and enter their names, email, phone and password etc. The data directly goes to users table. The password is stored in encrypted form not as a plain text to avoid security issues.
2.	When a user loses an item in a public area, they login the system and fill a repot form. They enter the item name, description, place where they found, date when lost and select the category of the item from a dropdown menu. This dropdown menu is dependent on categories table.
3.	Same when a user finds something. They login and fill a similar form. This table is dependent on categories table because every category has an expiry date stored in 