# City Care Hospital — Website + Django Backend + Help Chatbot

Static hospital website with a Django backend for forms, patient registration/login, and a floating help chatbot.

## Features added (frontend unchanged in look & feel)

- **Django backend** serving all existing HTML pages
- **Models & Admin**: Appointments, Contact messages, Career applications, Patient profiles, Chat logs
- **Form APIs**: appointment, contact, careers, register, login → data saved to SQLite
- **Help Chatbot**: floating widget on every page; keyword-based answers about appointments, emergency, departments, doctors, hours, insurance, etc. Logged in admin.

## Quick start

```bash
# Python 3.10+
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

### Admin panel
- URL: http://127.0.0.1:8000/admin/
- Username: `admin`
- Password: `admin123`

(Change password after first login.)

## Project structure

```
manage.py
hospital_project/     # Django settings & URLs
hospital/             # App: models, views, admin
templates/            # Original HTML pages
static/               # css, js, images, icons (unchanged)
db.sqlite3            # SQLite database
```

## Chatbot

Click the chat button (bottom-right). Ask things like:
- "How do I book an appointment?"
- "Emergency number?"
- "What departments do you have?"
- "Do you accept insurance?"

API: `POST /api/chatbot/` with JSON `{ "message": "...", "session_id": "..." }`

## Form endpoints

| Form        | Endpoint            |
|-------------|---------------------|
| Appointment | POST /api/appointment/ |
| Contact     | POST /api/contact/     |
| Careers     | POST /api/career/      |
| Register    | POST /api/register/    |
| Login       | POST /api/login/       |

## Notes

- Original design, content, and assets are preserved.
- Only small additions: `name` attributes on form inputs (for backend), enhanced form submit in `js/script.js`, and the chatbot widget injected by the same script.
- For production: set `DEBUG=False`, configure a real database, secret key, and static files (`collectstatic`).
