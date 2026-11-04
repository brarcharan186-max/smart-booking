"""Web routes for customers and staff."""
from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from . import booking
from .db import get_db

bp = Blueprint("main", __name__)


def _form_page(values=None, errors=None, status=200):
    return (
        render_template(
            "book.html",
            services=booking.SERVICES,
            time_slots=booking.TIME_SLOTS,
            today=date.today().isoformat(),
            values=values or {},
            errors=errors or [],
        ),
        status,
    )


@bp.get("/")
def book_form():
    return _form_page()


@bp.post("/book")
def book():
    data, errors = booking.validate_booking(request.form)
    if errors:
        return _form_page(data, errors, status=400)

    db = get_db()
    if booking.is_slot_taken(db, data["service"], data["date"], data["time"]):
        msg = (
            f"{data['service']} at {data['time']} on {data['date']} is already "
            "booked. Choose another time."
        )
        return _form_page(data, [msg], status=409)

    booking_id = booking.create_booking(db, data)
    return redirect(url_for("main.booked", booking_id=booking_id))


@bp.get("/booked/<int:booking_id>")
def booked(booking_id):
    appt = booking.get_booking(get_db(), booking_id)
    if appt is None:
        abort(404)
    return render_template("booked.html", appt=appt)


@bp.get("/staff")
def dashboard():
    rows = booking.list_bookings(get_db())
    active = sum(1 for r in rows if r["status"] == "active")
    return render_template("dashboard.html", bookings=rows, active=active)


@bp.post("/staff/cancel/<int:booking_id>")
def cancel(booking_id):
    if booking.cancel_booking(get_db(), booking_id):
        flash(f"Booking #{booking_id} cancelled. That time slot is free again.")
    else:
        flash(f"Booking #{booking_id} was already cancelled or does not exist.")
    return redirect(url_for("main.dashboard"))


@bp.get("/health")
def health():
    return {"status": "ok"}
