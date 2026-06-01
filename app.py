from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime, timedelta, date
from difflib import SequenceMatcher
from functools import wraps

app = Flask(__name__)
app.secret_key = 'lostfound2024secret'



def get_db():
    return mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = 'Mymysql#01300190',
        database = 'lost_and_found'
    )



LOCATIONS = [
    'Qissa Khwani Bazaar', 'Namak Mandi', 'Khyber Bazaar', 'Saddar Bazaar',
    'Dabgari Gardens', 'Meena Bazaar', 'Chowk Yadgar Bazaar', 'Firdous Bazaar',
    'Palosi Market', 'Gulbahar No. 1 Commercial Area', 'Gulbahar No. 2 Commercial Area',
    'Gulbahar No. 3 Commercial Area', 'Tehkal Market', 'Budni Bazaar', 'Karkhano Market',
    'Hayatabad Phase 1 Commercial Area', 'Hayatabad Phase 2 Commercial Area',
    'Hayatabad Phase 3 Commercial Area', 'Hayatabad Phase 4 Commercial Area',
    'Hayatabad Phase 5 Commercial Area', 'Hayatabad Phase 6 Commercial Area',
    'Lady Reading Hospital', 'Khyber Teaching Hospital', 'Hayatabad Medical Complex',
    'Pakistan Railway Hospital', 'Naseer Teaching Hospital', 'Rehman Medical Institute',
    'Northwest General Hospital', 'University of Peshawar', 'Islamia College University',
    'Edwardes College Peshawar', 'City University of Science and IT',
    'Frontier College Peshawar', 'Peshawar Medical College', 'Khyber Medical University',
    'Agriculture University Peshawar', 'University of Engineering and Technology Peshawar',
    'Institute of Management Sciences Peshawar', 'Sarhad University of Science and IT',
    'CECOS University Peshawar', 'Abasyn University Peshawar', 'Khyber Medical College',
    'Government College of Science Peshawar', 'Mahabat Khan Mosque', 'Sunehri Masjid',
    'Masjid Qasim Ali Khan', 'Eidgah Mosque Peshawar', 'Jamia Masjid Gulbahar',
    'Shahi Bagh Park', 'Wazir Bagh', 'Iqbal Park Peshawar', 'Peshawar Zoo',
    'Hayatabad Sports Complex', 'Peshawar Cantonment Railway Station', 'Peshawar Mor',
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def send_notification(user_id, message):
    db     = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO notifications (user_id, message) VALUES (%s, %s)',
        (user_id, message)
    )
    db.commit()
    cursor.close()
    db.close()


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def generate_matches(item_type, item_id):
    db     = get_db()
    cursor = db.cursor(dictionary=True)

    if item_type == 'lost':
        cursor.execute('SELECT * FROM lost_items WHERE lost_id = %s', (item_id,))
        new_item   = cursor.fetchone()
        cursor.execute('SELECT * FROM found_items WHERE status = %s', ('verified',))
        candidates = cursor.fetchall()
        for c in candidates:
            score = 0
            if new_item['category_id'] == c['category_id']:
                score += 50
            if new_item['location'].lower() == c['location'].lower():
                score += 30
            score += round(similarity(new_item['item_name'], c['item_name']) * 20, 2)
            score  = round(score, 2)
            if score >= 40:
                cursor.execute(
                    'SELECT match_id FROM matches WHERE lost_id=%s AND found_id=%s',
                    (item_id, c['found_id'])
                )
                if not cursor.fetchone():
                    cursor.execute(
                        'INSERT INTO matches (lost_id, found_id, similarity_score) VALUES (%s,%s,%s)',
                        (item_id, c['found_id'], score)
                    )

    elif item_type == 'found':
        cursor.execute('SELECT * FROM found_items WHERE found_id = %s', (item_id,))
        new_item   = cursor.fetchone()
        cursor.execute('SELECT * FROM lost_items WHERE status = %s', ('verified',))
        candidates = cursor.fetchall()
        for c in candidates:
            score = 0
            if c['category_id'] == new_item['category_id']:
                score += 50
            if c['location'].lower() == new_item['location'].lower():
                score += 30
            score += round(similarity(c['item_name'], new_item['item_name']) * 20, 2)
            score  = round(score, 2)
            if score >= 40:
                cursor.execute(
                    'SELECT match_id FROM matches WHERE lost_id=%s AND found_id=%s',
                    (c['lost_id'], item_id)
                )
                if not cursor.fetchone():
                    cursor.execute(
                        'INSERT INTO matches (lost_id, found_id, similarity_score) VALUES (%s,%s,%s)',
                        (c['lost_id'], item_id, score)
                    )

    db.commit()
    cursor.close()
    db.close()


def mark_expired():
    db     = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE found_items SET status='expired' WHERE status='verified' AND expiry_date < %s",
        (date.today(),)
    )
    db.commit()
    cursor.close()
    db.close()


def get_categories():
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM categories ORDER BY category_name')
    cats = cursor.fetchall()
    cursor.close()
    db.close()
    return cats

# ─────────────────────────────────────────────────────────────────────────────
# DECORATORS
# ─────────────────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────────────────────────────────────
# CONTEXT PROCESSOR — runs before every template
# ─────────────────────────────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    notif_count = 0
    if 'user_id' in session:
        try:
            db     = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                'SELECT COUNT(*) AS c FROM notifications WHERE user_id=%s AND is_read=FALSE',
                (session['user_id'],)
            )
            notif_count = cursor.fetchone()['c']
            cursor.close()
            db.close()
        except:
            pass
    return {'notif_count': notif_count}

# ─────────────────────────────────────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']

        db     = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user or not check_password_hash(user['password_hash'], password):
            flash('Incorrect email or password.', 'error')
            return redirect(url_for('login'))

        session.clear()
        session['user_id']   = user['user_id']
        session['user_name'] = user['full_name']
        session['role']      = user['role']

        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))

        flash(f"Welcome back, {user['full_name']}!", 'success')
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        email     = request.form['email'].strip().lower()
        phone     = request.form.get('phone', '').strip()
        password  = request.form['password']

        if not full_name or not email or not password:
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('register'))

        db     = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT user_id FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('This email is already registered.', 'error')
            cursor.close()
            db.close()
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (full_name, email, password_hash, phone) VALUES (%s,%s,%s,%s)',
            (full_name, email, hashed, phone)
        )
        db.commit()
        new_id = cursor.lastrowid
        cursor.close()
        db.close()

        session.clear()
        session['user_id']   = new_id
        session['user_name'] = full_name
        session['role']      = 'user'

        flash(f'Welcome, {full_name}! Your account has been created.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    db     = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('SELECT COUNT(*) AS c FROM lost_items')
    lost_count = cursor.fetchone()['c']

    cursor.execute('SELECT COUNT(*) AS c FROM found_items')
    found_count = cursor.fetchone()['c']

    cursor.execute("SELECT COUNT(*) AS c FROM lost_items WHERE status='returned'")
    returned_count = cursor.fetchone()['c']

    cursor.close()
    db.close()

    return render_template('home.html',
        total          = lost_count + found_count,
        lost_count     = lost_count,
        found_count    = found_count,
        returned_count = returned_count
    )


@app.route('/browse-lost')
def browse_lost():
    search      = request.args.get('search', '').strip()
    category_id = request.args.get('category_id', '')
    location    = request.args.get('location', '')
    status      = request.args.get('status', '')

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    query  = '''SELECT l.*, c.category_name, u.full_name
                FROM lost_items l
                JOIN categories c ON l.category_id = c.category_id
                JOIN users u ON l.user_id = u.user_id
                WHERE 1=1'''
    params = []

    if search:
        query += ' AND l.item_name LIKE %s'
        params.append(f'%{search}%')
    if category_id:
        query += ' AND l.category_id = %s'
        params.append(category_id)
    if location:
        query += ' AND l.location = %s'
        params.append(location)
    if status:
        query += ' AND l.status = %s'
        params.append(status)

    query += ' ORDER BY l.created_at DESC'
    cursor.execute(query, params)
    items = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('browse_lost.html',
        items       = items,
        categories  = get_categories(),
        locations   = LOCATIONS,
        search      = search,
        sel_cat     = category_id,
        sel_loc     = location,
        sel_status  = status
    )


@app.route('/browse-found')
def browse_found():
    search      = request.args.get('search', '').strip()
    category_id = request.args.get('category_id', '')
    location    = request.args.get('location', '')
    status      = request.args.get('status', '')

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    query  = '''SELECT f.*, c.category_name, u.full_name
                FROM found_items f
                JOIN categories c ON f.category_id = c.category_id
                JOIN users u ON f.user_id = u.user_id
                WHERE 1=1'''
    params = []

    if search:
        query += ' AND f.item_name LIKE %s'
        params.append(f'%{search}%')
    if category_id:
        query += ' AND f.category_id = %s'
        params.append(category_id)
    if location:
        query += ' AND f.location = %s'
        params.append(location)
    if status:
        query += ' AND f.status = %s'
        params.append(status)

    query += ' ORDER BY f.created_at DESC'
    cursor.execute(query, params)
    items = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('browse_found.html',
        items       = items,
        categories  = get_categories(),
        locations   = LOCATIONS,
        search      = search,
        sel_cat     = category_id,
        sel_loc     = location,
        sel_status  = status
    )


@app.route('/item/<string:item_type>/<int:item_id>')
def item_detail(item_type, item_id):
    db     = get_db()
    cursor = db.cursor(dictionary=True)

    if item_type == 'lost':
        cursor.execute('''
            SELECT l.*, c.category_name, u.full_name, u.phone
            FROM lost_items l
            JOIN categories c ON l.category_id = c.category_id
            JOIN users u ON l.user_id = u.user_id
            WHERE l.lost_id = %s
        ''', (item_id,))
    else:
        cursor.execute('''
            SELECT f.*, c.category_name, u.full_name, u.phone
            FROM found_items f
            JOIN categories c ON f.category_id = c.category_id
            JOIN users u ON f.user_id = u.user_id
            WHERE f.found_id = %s
        ''', (item_id,))

    item = cursor.fetchone()

    if not item:
        cursor.close()
        db.close()
        flash('Item not found.', 'error')
        return redirect(url_for('home'))

    # is the current user the founder of this item
    is_founder = (
        item_type == 'found' and
        'user_id' in session and
        session['user_id'] == item['user_id']
    )

    is_admin = session.get('role') == 'admin'

    # claims — only visible to founder and admin
    claims = []
    if item_type == 'found' and (is_founder or is_admin):
        cursor.execute('''
            SELECT cl.*, u.full_name AS claimer_name
            FROM claims cl
            JOIN users u ON cl.user_id = u.user_id
            WHERE cl.item_type = %s AND cl.item_id = %s
            ORDER BY cl.created_at DESC
        ''', (item_type, item_id))
        claims = cursor.fetchall()

    # verification questions — only question text shown to claimer, full row to founder/admin
    questions = []
    if item_type == 'found':
        cursor.execute(
            'SELECT * FROM verification_questions WHERE found_id = %s',
            (item_id,)
        )
        questions = cursor.fetchall()

    # check if current user already claimed this item
    already_claimed = False
    if 'user_id' in session and item_type == 'found':
        cursor.execute(
            'SELECT claim_id FROM claims WHERE item_type=%s AND item_id=%s AND user_id=%s',
            (item_type, item_id, session['user_id'])
        )
        already_claimed = cursor.fetchone() is not None

    cursor.close()
    db.close()

    return render_template('item_detail.html',
        item            = item,
        item_type       = item_type,
        item_id         = item_id,
        claims          = claims,
        questions       = questions,
        already_claimed = already_claimed,
        is_founder      = is_founder,
        is_admin        = is_admin
    )


@app.route('/claim', methods=['POST'])
@login_required
def submit_claim():
    item_type     = request.form['item_type']
    item_id       = int(request.form['item_id'])
    claim_message = request.form['claim_message'].strip()

    if not claim_message:
        flash('Please write your claim message.', 'error')
        return redirect(url_for('item_detail', item_type=item_type, item_id=item_id))

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    # check not already claimed
    cursor.execute(
        'SELECT claim_id FROM claims WHERE item_type=%s AND item_id=%s AND user_id=%s',
        (item_type, item_id, session['user_id'])
    )
    if cursor.fetchone():
        flash('You have already submitted a claim for this item.', 'error')
        cursor.close()
        db.close()
        return redirect(url_for('item_detail', item_type=item_type, item_id=item_id))

    cursor.execute(
        'INSERT INTO claims (item_type, item_id, user_id, claim_message) VALUES (%s,%s,%s,%s)',
        (item_type, item_id, session['user_id'], claim_message)
    )
    db.commit()
    cursor.close()
    db.close()

    flash('Your claim has been submitted. Admin will review it shortly.', 'success')
    return redirect(url_for('item_detail', item_type=item_type, item_id=item_id))


@app.route('/report-lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    if request.method == 'POST':
        item_name   = request.form['item_name'].strip()
        category_id = request.form['category_id']
        location    = request.form['location']
        date_lost   = request.form['date_lost']
        description = request.form.get('description', '').strip()

        if not item_name or not category_id or not location or not date_lost:
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('report_lost'))

        db     = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''INSERT INTO lost_items
               (user_id, category_id, item_name, description, location, date_lost)
               VALUES (%s,%s,%s,%s,%s,%s)''',
            (session['user_id'], category_id, item_name, description, location, date_lost)
        )
        db.commit()
        cursor.close()
        db.close()

        flash('Your lost item has been reported. Admin will review it shortly.', 'success')
        return redirect(url_for('browse_lost'))

    return render_template('report_lost.html',
        categories = get_categories(),
        locations  = LOCATIONS
    )


@app.route('/report-found', methods=['GET', 'POST'])
@login_required
def report_found():
    if request.method == 'POST':
        item_name   = request.form['item_name'].strip()
        category_id = int(request.form['category_id'])
        location    = request.form['location']
        date_found  = request.form['date_found']
        description = request.form.get('description', '').strip()

        if not item_name or not category_id or not location or not date_found:
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('report_found'))

        db     = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT expiry_days FROM categories WHERE category_id=%s', (category_id,))
        cat         = cursor.fetchone()
        expiry_date = (
            datetime.strptime(date_found, '%Y-%m-%d') + timedelta(days=cat['expiry_days'])
        ).strftime('%Y-%m-%d')

        cursor.execute(
            '''INSERT INTO found_items
               (user_id, category_id, item_name, description, location, date_found, expiry_date)
               VALUES (%s,%s,%s,%s,%s,%s,%s)''',
            (session['user_id'], category_id, item_name, description, location, date_found, expiry_date)
        )
        db.commit()
        found_id = cursor.lastrowid

        # save verification questions
        for i in range(1, 4):
            q = request.form.get(f'question_{i}', '').strip()
            a = request.form.get(f'answer_{i}', '').strip()
            if q and a:
                cursor.execute(
                    'INSERT INTO verification_questions (found_id, question, answer) VALUES (%s,%s,%s)',
                    (found_id, q, a)
                )
        db.commit()
        cursor.close()
        db.close()

        flash('Your found item has been reported. Admin will review it shortly.', 'success')
        return redirect(url_for('browse_found'))

    return render_template('report_found.html',
        categories = get_categories(),
        locations  = LOCATIONS
    )


@app.route('/notifications')
@login_required
def notifications():
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        'SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC',
        (session['user_id'],)
    )
    notifs = cursor.fetchall()

    # mark all as read
    cursor.execute(
        'UPDATE notifications SET is_read=TRUE WHERE user_id=%s',
        (session['user_id'],)
    )
    db.commit()
    cursor.close()
    db.close()

    return render_template('notifications.html', notifications=notifs)

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():
    mark_expired()

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    # stats
    cursor.execute('SELECT COUNT(*) AS c FROM lost_items')
    lost_count = cursor.fetchone()['c']

    cursor.execute('SELECT COUNT(*) AS c FROM found_items')
    found_count = cursor.fetchone()['c']

    cursor.execute("SELECT COUNT(*) AS c FROM lost_items WHERE status='returned'")
    returned_count = cursor.fetchone()['c']

    cursor.execute("SELECT COUNT(*) AS c FROM found_items WHERE status='expired' AND admin_action IS NULL")
    expired_count = cursor.fetchone()['c']

    cursor.execute("SELECT COUNT(*) AS c FROM claims WHERE status='pending'")
    claims_count = cursor.fetchone()['c']

    # pending items
    cursor.execute('''
        SELECT 'lost' AS type, lost_id AS id, item_name, location,
               date_lost AS date, status, c.category_name, u.full_name
        FROM lost_items l
        JOIN categories c ON l.category_id=c.category_id
        JOIN users u ON l.user_id=u.user_id
        WHERE l.status='pending'
        UNION ALL
        SELECT 'found', found_id, item_name, location,
               date_found, status, c.category_name, u.full_name
        FROM found_items f
        JOIN categories c ON f.category_id=c.category_id
        JOIN users u ON f.user_id=u.user_id
        WHERE f.status='pending'
        ORDER BY date DESC
    ''')
    pending_items = cursor.fetchall()

  
    # pending claims
    cursor.execute('''
        SELECT cl.*, u.full_name AS claimer_name,
               CASE WHEN cl.item_type='lost'
                    THEN (SELECT item_name FROM lost_items WHERE lost_id=cl.item_id)
                    ELSE (SELECT item_name FROM found_items WHERE found_id=cl.item_id)
               END AS item_name,
               CASE WHEN cl.item_type='found'
                    THEN (SELECT full_name FROM users
                          JOIN found_items ON users.user_id=found_items.user_id
                          WHERE found_items.found_id=cl.item_id)
                    ELSE NULL
               END AS founder_name
        FROM claims cl
        JOIN users u ON cl.user_id=u.user_id
        WHERE cl.status='pending'
        ORDER BY cl.created_at DESC
    ''')
    pending_claims = cursor.fetchall()

    # attach verification questions to each claim
    for claim in pending_claims:
        if claim['item_type'] == 'found':
            cursor.execute(
                'SELECT * FROM verification_questions WHERE found_id = %s',
                (claim['item_id'],)
            )
            claim['questions'] = cursor.fetchall()
        else:
            claim['questions'] = []

  
    cursor.execute('''
        SELECT m.*, l.item_name AS lost_name, l.location AS lost_loc,
               f.item_name AS found_name, f.location AS found_loc,
               c.category_name
        FROM matches m
        JOIN lost_items l ON m.lost_id=l.lost_id
        JOIN found_items f ON m.found_id=f.found_id
        JOIN categories c ON l.category_id=c.category_id
        ORDER BY m.matched_at DESC
    ''')
    matches = cursor.fetchall()

  
    cursor.execute('''
        SELECT f.*, c.category_name, u.full_name
        FROM found_items f
        JOIN categories c ON f.category_id=c.category_id
        JOIN users u ON f.user_id=u.user_id
        WHERE f.status='expired' AND f.admin_action IS NULL
        ORDER BY f.expiry_date ASC
    ''')
    expired_items = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('admin.html',
        lost_count     = lost_count,
        found_count    = found_count,
        returned_count = returned_count,
        expired_count  = expired_count,
        claims_count   = claims_count,
        pending_items  = pending_items,
        pending_claims = pending_claims,
        matches        = matches,
        expired_items  = expired_items
    )


@app.route('/admin/verify', methods=['POST'])
@admin_required
def admin_verify():
    item_type = request.form['type']
    item_id   = int(request.form['id'])

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    if item_type == 'lost':
        cursor.execute("UPDATE lost_items SET status='verified' WHERE lost_id=%s", (item_id,))
        cursor.execute('SELECT user_id, item_name FROM lost_items WHERE lost_id=%s', (item_id,))
        item = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        send_notification(item['user_id'],
            f"Your lost item report for '{item['item_name']}' has been verified.")
        generate_matches('lost', item_id)

    elif item_type == 'found':
        cursor.execute("UPDATE found_items SET status='verified' WHERE found_id=%s", (item_id,))
        cursor.execute('SELECT user_id, item_name FROM found_items WHERE found_id=%s', (item_id,))
        item = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        send_notification(item['user_id'],
            f"Your found item report for '{item['item_name']}' has been verified.")
        generate_matches('found', item_id)

    flash('Item verified and matches generated.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/reject', methods=['POST'])
@admin_required
def admin_reject():
    item_type = request.form['type']
    item_id   = int(request.form['id'])

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    if item_type == 'lost':
        cursor.execute('SELECT user_id, item_name FROM lost_items WHERE lost_id=%s', (item_id,))
        item = cursor.fetchone()
        cursor.execute('DELETE FROM lost_items WHERE lost_id=%s', (item_id,))
    else:
        cursor.execute('SELECT user_id, item_name FROM found_items WHERE found_id=%s', (item_id,))
        item = cursor.fetchone()
        cursor.execute('DELETE FROM found_items WHERE found_id=%s', (item_id,))

    db.commit()
    cursor.close()
    db.close()

    send_notification(item['user_id'],
        f"Your report for '{item['item_name']}' was rejected. Please contact us for more information.")

    flash('Item rejected and reporter notified.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/claim-action', methods=['POST'])
@admin_required
def admin_claim_action():
    claim_id = int(request.form['claim_id'])
    action   = request.form['action']

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('SELECT * FROM claims WHERE claim_id=%s', (claim_id,))
    claim = cursor.fetchone()

    cursor.execute('UPDATE claims SET status=%s WHERE claim_id=%s', (action, claim_id))

    if action == 'approved':
        # get item owner
        if claim['item_type'] == 'found':
            cursor.execute('SELECT user_id, item_name FROM found_items WHERE found_id=%s', (claim['item_id'],))
            item = cursor.fetchone()
            cursor.execute("UPDATE found_items SET status='returned' WHERE found_id=%s", (claim['item_id'],))
            send_notification(item['user_id'],
                f"Someone has claimed your found item '{item['item_name']}' and the claim has been approved. Please arrange to return it.")
        else:
            cursor.execute('SELECT user_id, item_name FROM lost_items WHERE lost_id=%s', (claim['item_id'],))
            item = cursor.fetchone()
            cursor.execute("UPDATE lost_items SET status='returned' WHERE lost_id=%s", (claim['item_id'],))
            send_notification(item['user_id'],
                f"A match for your lost item '{item['item_name']}' has been found and approved.")

        # notify the claimer
        send_notification(claim['user_id'],
            f"Your claim has been approved. Please contact the admin to collect your item.")

    else:
        send_notification(claim['user_id'],
            f"Your claim could not be approved at this time.")

    db.commit()
    cursor.close()
    db.close()

    flash('Claim updated and user notified.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/match-action', methods=['POST'])
@admin_required
def admin_match_action():
    match_id = int(request.form['match_id'])
    action   = request.form['action']

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('UPDATE matches SET match_status=%s WHERE match_id=%s', (action, match_id))

    if action == 'confirmed':
        cursor.execute('SELECT lost_id, found_id FROM matches WHERE match_id=%s', (match_id,))
        match = cursor.fetchone()

        cursor.execute('SELECT user_id, item_name FROM lost_items WHERE lost_id=%s', (match['lost_id'],))
        lost_item = cursor.fetchone()

        cursor.execute('SELECT user_id, item_name FROM found_items WHERE found_id=%s', (match['found_id'],))
        found_item = cursor.fetchone()

        cursor.execute("UPDATE lost_items SET status='returned' WHERE lost_id=%s", (match['lost_id'],))
        cursor.execute("UPDATE found_items SET status='returned' WHERE found_id=%s", (match['found_id'],))

        send_notification(lost_item['user_id'],
            f"Great news! A match has been confirmed for your lost item '{lost_item['item_name']}'. Please contact admin to collect it.")
        send_notification(found_item['user_id'],
            f"The lost item '{found_item['item_name']}' you found has been matched with its owner. Please contact admin to return it.")

    db.commit()
    cursor.close()
    db.close()

    flash('Match updated and users notified.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/expired-action', methods=['POST'])
@admin_required
def admin_expired_action():
    found_id     = int(request.form['found_id'])
    admin_action = request.form['admin_action']
    admin_note   = request.form.get('admin_note', '').strip()

    db     = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('SELECT user_id, item_name FROM found_items WHERE found_id=%s', (found_id,))
    item = cursor.fetchone()

    cursor.execute(
        'UPDATE found_items SET admin_action=%s, admin_note=%s WHERE found_id=%s',
        (admin_action, admin_note, found_id)
    )
    db.commit()
    cursor.close()
    db.close()

    action_msg = admin_action.replace('_', ' ').title()
    send_notification(item['user_id'],
        f"Your found item '{item['item_name']}' has expired and has been {action_msg}.")

    flash('Action saved and user notified.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
