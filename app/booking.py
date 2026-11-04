"""Booking rules: validation, the double-booking check, and database actions."""
from datetime import date

SERVICES = ["Consultation", "Haircut", "Follow-up visit", "Massage"]

# Half-hour slots from 09:00 to 16:30.
TIME_SLOTS = [f"{h:02d}:{m:02d}" for h in range(9, 17) for m in (0, 30)]


def validate_booking(form):
    """Check the form. Returns (clean_data, errors). Nothing is saved here."""
    data = {
        "customer_name": form.get("customer_name", "").strip(),
        "service": form.get("service", "").strip(),
        "date": form.get("date", "").strip(),
        "time": form.get("time", "").strip(),
    }
    errors = []

    if not data["customer_name"]:
        errors.append("Enter your name.")
    elif len(data["customer_name"]) > 80:
        errors.append("Name must be 80 characters or fewer.")

    if not data["service"]:
        errors.append("Choose a service.")
    elif data["service"] not in SERVICES:
        errors.append("Choose a service from the list.")

    if not data["date"]:
        errors.append("Choose a date.")
    else:
        try:
            if date.fromisoformat(data["date"]) < date.today():
                errors.append("Choose today or a future date.")
        except ValueError:
            errors.append("Enter the date as YYYY-MM-DD.")

    if not data["time"]:
        errors.append("Choose a time.")
    elif data["time"] not in TIME_SLOTS:
        errors.append("Choose a time between 09:00 and 16:30.")

    return data, errors


def is_slot_taken(db, service, date_, time):
    """True if this service already has an ACTIVE booking at this date and time."""
    row = db.execute(
        "SELECT 1 FROM appointments "
        "WHERE service = ? AND date = ? AND time = ? AND status = 'cancelled'",
        (service, date_, time),
    ).fetchone()
    return row is not None


def create_booking(db, data):
    cur = db.execute(
        "INSERT INTO appointments (customer_name, service, date, time) "
        "VALUES (?, ?, ?, ?)",
        (data["customer_name"], data["service"], data["date"], data["time"]),
    )
    db.commit()
    return cur.lastrowid


def get_booking(db, booking_id):
    return db.execute(
        "SELECT * FROM appointments WHERE id = ?", (booking_id,)
    ).fetchone()


def list_bookings(db):
    return db.execute(
        "SELECT * FROM appointments ORDER BY date, time, service"
    ).fetchall()


def cancel_booking(db, booking_id):
    """Mark a booking as cancelled. Returns True if an active booking was cancelled."""
    cur = db.execute(
        "UPDATE appointments SET status = 'cancelled' "
        "WHERE id = ? AND status = 'active'",
        (booking_id,),
    )
    db.commit()
    return cur.rowcount == 1
