"""
Slot Booking Web Application
Flask + SQLite (Local Database)
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'slot-booking-secret-key-2026')

DATABASE = 'slot_booking.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                is_booked INTEGER DEFAULT 0,
                booked_by TEXT DEFAULT NULL,
                booked_email TEXT DEFAULT NULL,
                booked_at DATETIME DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Check if we have data
        cur.execute("SELECT COUNT(*) FROM slots")
        if cur.fetchone()[0] == 0:
            # Seed data
            for day_offset in range(3):
                for hour in range(9, 17):
                    date_val = f"date('now', '+{day_offset} day')"
                    cur.execute(f'''
                        INSERT INTO slots (slot_date, start_time, end_time) 
                        VALUES ({date_val}, '{hour:02d}:00:00', '{hour+1:02d}:00:00')
                    ''')
        db.commit()

# Call init_db on startup
with app.app_context():
    init_db()


# ─── Helper ─────────────────────────────────────────────────────────
def format_time(t_str):
    """Convert time string like '09:00:00' to '09:00 AM'."""
    if not isinstance(t_str, str):
        return str(t_str)
    try:
        t = datetime.strptime(t_str, '%H:%M:%S').time()
        hours, minutes = t.hour, t.minute
        period = 'AM' if hours < 12 else 'PM'
        display_hour = hours % 12 or 12
        return f"{display_hour}:{minutes:02d} {period}"
    except ValueError:
        return t_str

def format_date(d_str):
    """Format a date string like 'Y-m-d' to a readable string."""
    if not isinstance(d_str, str):
        return str(d_str)
    try:
        d = datetime.strptime(d_str, '%Y-%m-%d')
        return d.strftime('%A, %B %d, %Y')
    except ValueError:
        return d_str

# ─── Routes ─────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Show all available (unbooked) slots grouped by date."""
    cur = get_db().cursor()
    cur.execute(
        "SELECT * FROM slots WHERE is_booked = 0 ORDER BY slot_date, start_time"
    )
    slots_rows = cur.fetchall()
    
    # Group slots by date
    grouped = {}
    for row in slots_rows:
        slot = dict(row)
        date_key = slot['slot_date']
        if date_key not in grouped:
            grouped[date_key] = {
                'date_label': format_date(date_key),
                'slots': []
            }
        slot['start_label'] = format_time(slot['start_time'])
        slot['end_label'] = format_time(slot['end_time'])
        grouped[date_key]['slots'].append(slot)

    return render_template('index.html', grouped=grouped)

@app.route('/booked')
def booked():
    """Show all booked slots."""
    cur = get_db().cursor()
    cur.execute(
        "SELECT * FROM slots WHERE is_booked = 1 ORDER BY slot_date, start_time"
    )
    slots_rows = cur.fetchall()
    
    slots = []
    for row in slots_rows:
        slot = dict(row)
        slot['start_label'] = format_time(slot['start_time'])
        slot['end_label'] = format_time(slot['end_time'])
        slot['date_label'] = format_date(slot['slot_date'])
        slots.append(slot)

    return render_template('booked.html', slots=slots)

@app.route('/book/<int:slot_id>', methods=['GET', 'POST'])
def book(slot_id):
    """Book a specific slot."""
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        if not name or not email:
            flash('Please provide both your name and email.', 'error')
            return redirect(url_for('book', slot_id=slot_id))

        # Check slot is still available
        cur.execute("SELECT * FROM slots WHERE id = ? AND is_booked = 0", (slot_id,))
        row = cur.fetchone()
        if not row:
            flash('Sorry, this slot is no longer available.', 'error')
            return redirect(url_for('index'))
            
        slot = dict(row)

        # Book the slot
        cur.execute(
            "UPDATE slots SET is_booked = 1, booked_by = ?, booked_email = ?, booked_at = ? WHERE id = ?",
            (name, email, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), slot_id)
        )
        db.commit()

        return render_template(
            'book_success.html',
            name=name,
            slot_date=format_date(slot['slot_date']),
            start_time=format_time(slot['start_time']),
            end_time=format_time(slot['end_time']),
        )

    # GET — show booking form
    cur.execute("SELECT * FROM slots WHERE id = ? AND is_booked = 0", (slot_id,))
    row = cur.fetchone()

    if not row:
        flash('This slot is no longer available.', 'error')
        return redirect(url_for('index'))
        
    slot = dict(row)

    slot['start_label'] = format_time(slot['start_time'])
    slot['end_label'] = format_time(slot['end_time'])
    slot['date_label'] = format_date(slot['slot_date'])

    return render_template('book_form.html', slot=slot)

@app.route('/cancel/<int:slot_id>', methods=['POST'])
def cancel(slot_id):
    """Cancel a booking and make the slot available again."""
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE slots SET is_booked = 0, booked_by = NULL, booked_email = NULL, booked_at = NULL WHERE id = ?",
        (slot_id,)
    )
    db.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('booked'))

# ─── Run ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
