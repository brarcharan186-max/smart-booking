from datetime import date, timedelta

from app.db import get_db


def count_bookings(app, status=None):
    with app.app_context():
        sql = "SELECT COUNT(*) FROM appointments"
        args = ()
        if status:
            sql += " WHERE status = ?"
            args = (status,)
        return get_db().execute(sql, args).fetchone()[0]


def test_booking_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Book an appointment" in res.data


def test_valid_booking_is_saved(app, make_booking):
    res = make_booking(customer_name="Asha")
    assert res.status_code == 302
    assert "/booked/1" in res.headers["Location"]
    assert count_bookings(app, "active") == 1


def test_confirmation_page_shows_booking(client, make_booking):
    make_booking(customer_name="Asha")
    res = client.get("/booked/1")
    assert res.status_code == 200
    assert b"Asha" in res.data


def test_missing_fields_are_rejected(app, client):
    res = client.post("/book", data={"customer_name": "", "service": "", "date": "", "time": ""})
    assert res.status_code == 400
    assert b"Enter your name." in res.data
    assert b"Choose a time." in res.data
    assert count_bookings(app) == 0


def test_double_booking_is_rejected(app, make_booking):
    make_booking(customer_name="First")
    res = make_booking(customer_name="Second")
    assert res.status_code == 409
    assert b"already booked" in res.data
    assert count_bookings(app) == 1


def test_same_time_different_service_is_allowed(app, make_booking):
    make_booking(service="Consultation")
    res = make_booking(service="Haircut")
    assert res.status_code == 302
    assert count_bookings(app, "active") == 2


def test_past_date_is_rejected(app, make_booking):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    res = make_booking(date=yesterday)
    assert res.status_code == 400
    assert count_bookings(app) == 0


def test_invalid_time_is_rejected(app, make_booking):
    res = make_booking(time="03:15")
    assert res.status_code == 400
    assert count_bookings(app) == 0


def test_saved_bookings_appear_on_dashboard(client, make_booking):
    make_booking(customer_name="Asha", time="09:00")
    make_booking(customer_name="Ben", time="10:30")
    res = client.get("/staff")
    assert res.status_code == 200
    assert b"Asha" in res.data and b"Ben" in res.data


def test_cancel_frees_the_slot(app, client, make_booking):
    make_booking()
    res = client.post("/staff/cancel/1")
    assert res.status_code == 302
    assert count_bookings(app, "cancelled") == 1

    # The same slot can now be booked again.
    res = make_booking(customer_name="New Customer")
    assert res.status_code == 302
    assert count_bookings(app, "active") == 1


def test_sql_injection_text_is_stored_as_plain_text(app, client, make_booking):
    make_booking(customer_name="Robert'); DROP TABLE appointments;--")
    assert count_bookings(app) == 1
    assert b"DROP TABLE" in client.get("/staff").data
