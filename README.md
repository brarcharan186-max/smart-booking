# Smart Appointment Booking and Management System

DEVP-600 project by Chandermukhi and Charan Kamal.

Customers book a service, date and time online. Staff view and cancel bookings. Double bookings are blocked. Every change is tested with pytest in GitHub Actions and packaged with Docker.

## Project structure

```
app/
  __init__.py      Flask app factory
  booking.py       booking rules (validation, double-booking check)
  routes.py        web pages: /, /book, /booked/<id>, /staff
  db.py            SQLite connection
  schema.sql       appointments table
  templates/       HTML pages
  static/style.css styles
tests/             pytest tests
.github/workflows/ci.yml   GitHub Actions: tests, then Docker build
Dockerfile, docker-compose.yml
docs/backlog.md    user stories for GitHub Projects
```

## 1. Install (once)

- Python 3.12: https://www.python.org/downloads/ (on Windows, tick "Add Python to PATH")
- Git: https://git-scm.com/downloads
- Docker Desktop: https://www.docker.com/products/docker-desktop/
- VS Code: https://code.visualstudio.com/

## 2. Run the app on your laptop

Open a terminal in this folder.

**Windows (PowerShell)**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app run --debug
```

**Mac / Linux**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Open http://127.0.0.1:5000 to book, and http://127.0.0.1:5000/staff for the staff dashboard.

If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

## 3. Run the tests

With the virtual environment active:
```
pytest -v
```
All 11 tests should pass.

## 4. Run with Docker

Start Docker Desktop first, then:
```
copy .env.example .env        (Mac/Linux: cp .env.example .env)
docker compose up --build
```
Open http://localhost:8000. Stop with `Ctrl+C`. Bookings are kept in the `booking-data` volume, so they survive a restart. To wipe them: `docker compose down -v`.

## 5. Put it on GitHub

Create an empty repository on GitHub (no README), then:
```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/smart-booking.git
git push -u origin main
```
Open the **Actions** tab on GitHub to see the workflow run. Add your partner under **Settings > Collaborators**.

### Working with branches and pull requests

```
git checkout -b feature/staff-dashboard
# make changes
git add .
git commit -m "Add staff dashboard"
git push -u origin feature/staff-dashboard
```
Then open a pull request on GitHub. Merge it only when the CI checks are green.

To block merges when tests fail: **Settings > Branches > Add rule** for `main`, tick "Require status checks to pass", and select "Run pytest" and "Build Docker image".

## 6. Demo: show the pipeline stopping a bad change

1. On a new branch, open `app/booking.py` and change `status = 'active'` in `is_slot_taken` to `status = 'cancelled'`.
2. Commit, push and open a pull request. The "Run pytest" job fails and the Docker job is skipped.
3. Change it back, commit and push. Both jobs turn green.

Take screenshots of the red and green runs for your report.

## Security notes

- All SQL uses `?` placeholders (parameterized queries).
- Form input is validated on the server.
- `SECRET_KEY` comes from an environment variable or `.env`, which is not committed.
- This is a student prototype: use fake customer data only. The staff page has no login.
