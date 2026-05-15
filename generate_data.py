import csv
import random
import os
from datetime import date, timedelta, datetime

os.makedirs('csv_data', exist_ok=True)

male_names = [
    'Ahmed', 'Ali', 'Hassan', 'Usman', 'Bilal', 'Farhan', 'Asad',
    'Tariq', 'Imran', 'Zubair', 'Kamran', 'Saad', 'Hamza', 'Waqar',
    'Junaid', 'Adeel', 'Fahad', 'Faisal', 'Rizwan', 'Shahid',
    'Waseem', 'Naveed', 'Umer', 'Babar', 'Arslan', 'Talha', 'Yasir',
    'Noman', 'Danish', 'Awais', 'Zain', 'Aamir', 'Rehan', 'Salman',
    'Ihsan', 'Murad', 'Sajid', 'Khalid', 'Nasir', 'Zahid'
]

female_names = [
    'Fatima', 'Ayesha', 'Zainab', 'Maryam', 'Sara', 'Sana', 'Hira',
    'Nadia', 'Amna', 'Rabia', 'Bushra', 'Sadia', 'Farah', 'Mehwish',
    'Lubna', 'Iqra', 'Mahnoor', 'Nimra', 'Sidra', 'Uzma', 'Sobia',
    'Kiran', 'Shazia', 'Aiman', 'Noor', 'Saima', 'Rukhsana', 'Gulnaz'
]

last_names = [
    'Khan', 'Ahmed', 'Ali', 'Rehman', 'Malik', 'Shah', 'Hussain',
    'Qureshi', 'Akhtar', 'Baig', 'Mirza', 'Siddiqui', 'Chaudhry',
    'Ansari', 'Sheikh', 'Bukhari', 'Khattak', 'Yousaf', 'Nawaz',
    'Afridi', 'Shinwari', 'Mohmand', 'Durrani', 'Bangash', 'Jadoon',
    'Swati', 'Khalil', 'Marwat', 'Wazir', 'Dawar'
]

phone_prefixes = [
    '0300', '0301', '0302', '0303', '0310',
    '0311', '0312', '0313', '0320', '0321',
    '0322', '0333', '0334', '0345', '0346'
]


locations = [
    'Qissa Khwani Bazaar',
    'Namak Mandi',
    'Khyber Bazaar',
    'Saddar Bazaar',
    'Dabgari Gardens',
    'Meena Bazaar',
    'Chowk Yadgar Bazaar',
    'Firdous Bazaar',
    'Palosi Market',
    'Gulbahar No. 1',
    'Gulbahar No. 2',
    'Gulbahar No. 3',
    'Tehkal Market',
    'Budni Bazaar',
    'Karkhano Market',
    
    'Hayatabad Phase 1',
    'Hayatabad Phase 2',
    'Hayatabad Phase 3',
    'Hayatabad Phase 4',
    'Hayatabad Phase 5',
    'Hayatabad Phase 6',
    'Lady Reading Hospital',
    'Khyber Teaching Hospital',
    'Hayatabad Medical Complex',
    'Pakistan Railway Hospital',
    'Naseer Teaching Hospital',
    'Rehman Medical Institute',
    'Northwest General Hospital',
    'University of Peshawar',
    'Islamia College University',
    'Edwardes College Peshawar',
    'City University of Science and IT',
    'Frontier College Peshawar',
    'Peshawar Medical College',
    'Khyber Medical University',
    'Agriculture University Peshawar',
    'University of Engineering and Technology Peshawar',
    'Institute of Management Sciences Peshawar',
    'Sarhad University of Science and IT',
    'CECOS University Peshawar',
    'Abasyn University Peshawar',
    'Khyber Medical College',
    'Government College of Science Peshawar',
    'Mahabat Khan Mosque',
    'Sunehri Masjid',
    'Masjid Qasim Ali Khan',
    'Eidgah Mosque Peshawar',
    'Jamia Masjid Gulbahar',
    'Shahi Bagh Park',
    'Wazir Bagh',
    'Iqbal Park Peshawar',
    'Peshawar Zoo',
    'Hayatabad Sports Complex',
    'Peshawar Cantonment Railway Station',
]

categories = [
    (1,  'CNIC / National ID Card',    10),
    (2,  'Student ID Card',            15),
    (3,  'Mobile Phone',               45),
    (4,  'Laptop',                     60),
    (5,  'Wallet / Purse',             20),
    (6,  'Keys',                       15),
    (7,  'Bag / Backpack',             30),
    (8,  'Books & Stationery',         20),
    (9,  'Clothing & Accessories',     25),
    (10, 'Watch & Glasses',            30),
    (11, 'Jewellery',                  45),
    (12, 'Documents & Certificates',   10),
    (13, 'Charger & Earphones',        20),
    (14, 'Bank Cards',                 10),
    (15, 'Other',                      30),
]

category_expiry = {c[0]: c[2] for c in categories}

category_items = {
    1:  ['CNIC', 'National ID Card', 'Computerized ID Card'],
    2:  ['Student ID Card', 'University Card', 'College ID Card'],
    3:  ['Mobile Phone', 'Android Phone', 'Samsung Phone', 'iPhone', 'Vivo Phone', 'Oppo Phone'],
    4:  ['Laptop', 'Dell Laptop', 'HP Laptop', 'Lenovo Laptop', 'Acer Laptop'],
    5:  ['Wallet', 'Purse', 'Leather Wallet', 'Ladies Purse', 'Gents Wallet'],
    6:  ['House Keys', 'Car Keys', 'Motorcycle Keys', 'Office Keys', 'Key Bundle'],
    7:  ['Backpack', 'Handbag', 'School Bag', 'University Bag', 'Shoulder Bag', 'Cloth Bag'],
    8:  ['Notebook', 'Textbook', 'Documents Folder', 'Stationery Pouch', 'Register', 'Drawing File'],
    9:  ['Shawl', 'Dupatta', 'Jacket', 'Waistcoat', 'Sweater', 'Cap', 'Scarf', 'Shalwar Kameez'],
    10: ['Wristwatch', 'Spectacles', 'Sunglasses', 'Reading Glasses'],
    11: ['Gold Ring', 'Silver Bracelet', 'Gold Necklace', 'Earrings', 'Bangle', 'Gold Chain'],
    12: ['Degree Certificate', 'Result Card', 'Mark Sheet', 'Domicile Certificate', 'Birth Certificate'],
    13: ['Mobile Charger', 'Earphones', 'Charging Cable', 'Power Bank', 'Earbuds', 'Data Cable'],
    14: ['ATM Card', 'Debit Card', 'Credit Card', 'HBL Card', 'Meezan Bank Card', 'UBL Card'],
    15: ['Umbrella', 'Tiffin Box', 'Water Bottle', 'Prayer Beads', 'Thermos', 'Lunch Box'],
}

category_descriptions = {
    1: [
        'CNIC card found near the main entrance, belongs to a male person',
        'Female CNIC found on the floor near the counter',
        'Old CNIC card found in a plastic cover near the gate',
        'CNIC card found on the bench, name visible on it',
        'Computerized ID card found near the reception area',
    ],
    2: [
        'Student ID card with photo found near the canteen',
        'University card found on a bench near the library',
        'College ID card found near the main gate',
        'Student card found in the parking area with photo visible',
        'ID card found near the classroom door',
    ],
    3: [
        'Black Android phone found switched on near the entrance',
        'iPhone with cracked screen found on the seat',
        'Samsung phone with blue cover found on the floor',
        'Vivo phone found near the charging point',
        'Mobile phone with broken screen found near the bus stop',
        'Android phone found switched off near the washroom',
    ],
    4: [
        'Dell laptop in black bag found near the library',
        'HP laptop without charger found on the table',
        'Lenovo laptop found near the canteen area',
        'Laptop with stickers found in the classroom',
        'Acer laptop found near the main gate in a bag',
    ],
    5: [
        'Brown leather wallet with some cash inside found on floor',
        'Ladies purse with ID card and cards inside found on seat',
        'Gents wallet with visiting cards found near entrance',
        'Black wallet found near the reception counter',
        'Wallet with cash and CNIC found near the gate',
    ],
    6: [
        'Bundle of keys with keychain found on the floor',
        'Motorcycle keys with remote found near the parking area',
        'House keys with a green tag found near the gate',
        'Car keys found on the bench near the entrance',
        'Office keys with tag found near the reception',
    ],
    7: [
        'Black backpack with books inside found near the gate',
        'Ladies handbag with personal items found on the seat',
        'School bag with notebooks found near the bus stop',
        'University bag found in the cafeteria area',
        'Shoulder bag with clothes inside found near entrance',
    ],
    8: [
        'Biology textbook with student name written on it',
        'Notebook with detailed notes found on the bench',
        'Folder with printed documents found near library',
        'Stationery pouch with pens and pencils found on floor',
        'Drawing file with papers found near the gate',
    ],
    9: [
        'Brown shawl left on the bench near the entrance',
        'Ladies dupatta found near the prayer area',
        'Black jacket left on a chair inside the hall',
        'Woolen cap found near the main gate',
        'Green scarf found near the reception area',
    ],
    10: [
        'Silver wristwatch found near the reception counter',
        'Spectacles in hard case found on the table',
        'Sunglasses found near the parking area',
        'Reading glasses found near the prayer area',
        'Black wristwatch found on the bench',
    ],
    11: [
        'Gold ring found near the washroom entrance',
        'Silver bracelet found on the floor near counter',
        'Gold necklace found near the main entrance',
        'Pair of gold earrings found near the chair',
        'Gold bangle found near the prayer area',
    ],
    12: [
        'Degree certificate in folder found near the office',
        'Result card with student details found on bench',
        'Domicile certificate found near the main counter',
        'Mark sheet found near the library entrance',
        'Birth certificate found in an envelope near the gate',
    ],
    13: [
        'Samsung mobile charger found near a charging socket',
        'White earphones found on the table near canteen',
        'Charging cable found near the power socket',
        'Power bank found on the seat near the entrance',
        'Earbuds with case found near the library',
    ],
    14: [
        'HBL ATM card found near the ATM machine',
        'Meezan Bank debit card found on the floor',
        'UBL credit card found near the reception counter',
        'Bank debit card found in the parking area',
        'ATM card found near the main entrance of the building',
    ],
    15: [
        'Black umbrella found near the main entrance',
        'Tiffin box with food inside found in the cafeteria',
        'Water bottle found near the bench outside',
        'Prayer beads found near the mosque area',
        'Thermos flask found near the seating area',
    ],
}



def random_name():
    gender = random.choice(['male', 'female'])
    first  = random.choice(male_names if gender == 'male' else female_names)
    last   = random.choice(last_names)
    return f"{first} {last}"

def random_phone():
    prefix = random.choice(phone_prefixes)
    number = random.randint(1000000, 9999999)
    return f"{prefix}{number}"

used_emails = set()
def random_email(name):
    parts  = name.lower().split()
    first  = parts[0]
    last   = parts[1]
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    while True:
        suffix = random.randint(1, 9999)
        email  = f"{first}.{last}{suffix}@{random.choice(domains)}"
        if email not in used_emails:
            used_emails.add(email)
            return email

def random_password_hash():
    chars = 'abcdef0123456789'
    return ''.join(random.choices(chars, k=64))

def random_datetime(start, end=None):
    if end is None:
        end = date.today()
    if isinstance(start, str):
        start = date.fromisoformat(start)
    if isinstance(end, str):
        end   = date.fromisoformat(end)
    delta = (end - start).days
    if delta <= 0:
        delta = 1
    rand_days    = random.randint(0, delta)
    rand_seconds = random.randint(0, 86399)
    result = datetime.combine(start, datetime.min.time()) + timedelta(days=rand_days, seconds=rand_seconds)
    return result.strftime('%Y-%m-%d %H:%M:%S')

def random_date(start_days_ago, end_days_ago=0):
    start = date.today() - timedelta(days=start_days_ago)
    end   = date.today() - timedelta(days=end_days_ago)
    delta = (end - start).days
    if delta <= 0:
        delta = 1
    return start + timedelta(days=random.randint(0, delta))

with open('csv_data/categories.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['category_id', 'category_name', 'expiry_days'])
    writer.writerows(categories)

print("categories.csv done — 15 rows")

users = []
for i in range(1, 61):
    name = random_name()
    users.append({
        'user_id':       i,
        'full_name':     name,
        'email':         random_email(name),
        'password_hash': random_password_hash(),
        'phone':         random_phone(),
        'role':          'admin' if i == 1 else 'user',
        'created_at':    random_datetime(date.today() - timedelta(days=365)),
    })

with open('csv_data/users.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=users[0].keys())
    writer.writeheader()
    writer.writerows(users)

print("users.csv done — 60 rows")

lost_items = []
for i in range(1, 101):
    cat_id    = random.randint(1, 15)
    date_lost = random_date(180, 0)

    lost_items.append({
        'lost_id':     i,
        'user_id':     random.randint(2, 60),
        'category_id': cat_id,
        'item_name':   random.choice(category_items[cat_id]),
        'description': random.choice(category_descriptions[cat_id]),
        'location':    random.choice(locations),
        'date_lost':   date_lost.strftime('%Y-%m-%d'),
        'status':      random.choice(['pending', 'verified', 'returned']),
        'created_at':  random_datetime(date_lost),
    })

with open('csv_data/lost_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=lost_items[0].keys())
    writer.writeheader()
    writer.writerows(lost_items)

print("lost_items.csv done — 100 rows")


admin_actions = ['archived', 'sent_to_authority', 'donated', 'destroyed']
admin_notes = [
    'Item was not claimed within the allowed time period',
    'Sent to the relevant authority as per policy',
    'Donated to a local charity after expiry',
    'Item was destroyed as it had no further use',
    'Handed over to the concerned department',
    'No one came to claim this item after multiple announcements',
    'Sent to NADRA office for further action',
    'Given to nearby mosque for safekeeping',
]

found_items = []
for i in range(1, 101):
    cat_id     = random.randint(1, 15)
    date_found = random_date(180, 0)
    expiry     = date_found + timedelta(days=category_expiry[cat_id])

    if expiry < date.today():
        status = random.choice(['expired', 'returned', 'verified'])
    else:
        status = random.choice(['pending', 'verified'])

    if status == 'expired':
        admin_action = random.choice(admin_actions)
        admin_note   = random.choice(admin_notes)
    else:
        admin_action = ''
        admin_note   = ''

    found_items.append({
        'found_id':     i,
        'user_id':      random.randint(2, 60),
        'category_id':  cat_id,
        'item_name':    random.choice(category_items[cat_id]),
        'description':  random.choice(category_descriptions[cat_id]),
        'location':     random.choice(locations),
        'date_found':   date_found.strftime('%Y-%m-%d'),
        'expiry_date':  expiry.strftime('%Y-%m-%d'),
        'status':       status,
        'admin_action': admin_action,
        'admin_note':   admin_note,
        'created_at':   random_datetime(date_found),
    })

with open('csv_data/found_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=found_items[0].keys())
    writer.writeheader()
    writer.writerows(found_items)

print("found_items.csv done — 100 rows")

matches    = []
used_pairs = set()

for i in range(1, 61):
    attempts = 0
    while True:
        lost_id  = random.randint(1, 100)
        found_id = random.randint(1, 100)
        if (lost_id, found_id) not in used_pairs:
            used_pairs.add((lost_id, found_id))
            break
        attempts += 1
        if attempts > 1000:
            break

    matched_date = random_date(90, 0)
    matches.append({
        'match_id':         i,
        'lost_id':          lost_id,
        'found_id':         found_id,
        'similarity_score': round(random.uniform(60.00, 99.99), 2),
        'match_status':     random.choice(['pending', 'confirmed', 'rejected']),
        'matched_at':       random_datetime(matched_date),
    })

with open('csv_data/matches.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=matches[0].keys())
    writer.writeheader()
    writer.writerows(matches)

print("matches.csv done — 60 rows")
print("\nAll 5 CSV files saved inside csv_data folder")
print("Total rows generated:")
print(f"  categories : 15")
print(f"  users      : 60")
print(f"  lost_items : 100")
print(f"  found_items: 100")
print(f"  matches    : 60")