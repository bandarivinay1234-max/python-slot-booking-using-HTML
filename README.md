# 📅 SlotBook — Slot Booking Web Application

A modern slot booking web application built with **Python Flask** and **MySQL**.

## Features

- 🟢 **View Available Slots** — Browse time slots grouped by date
- 📝 **Book a Slot** — Reserve a slot with your name and email
- 📋 **View Booked Slots** — See all confirmed bookings
- ❌ **Cancel Booking** — Free up a slot if plans change

## Tech Stack

- **Backend:** Python 3, Flask, Flask-MySQLdb
- **Database:** MySQL
- **Frontend:** HTML5, CSS3 (dark theme with glassmorphism)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/slot-booking-app.git
cd slot-booking-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

Make sure MySQL is running and then execute:

```sql
source schema.sql
```

This creates the `slot_booking` database with sample time slots.

### 5. Configure (Optional)

If your MySQL credentials differ from `root` with no password, update `app.py` lines 14–18 or set environment variables:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=slot_booking
```

### 6. Run the App

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

## Screenshots

| Available Slots | Booking Form | Booked Slots |
|---|---|---|
| View & book slots | Enter name & email | Manage bookings |

## License

MIT
