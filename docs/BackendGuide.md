# Buena Vista Cottage — Backend Developer Guide
**Developer:** Victor  
**Stack:** Django · Django REST Framework · PostgreSQL  
**Role:** Backend only — Samuel handles React (web) and React Native (mobile)

---

## Overview

You are building the Django REST API that powers **both** the web app (React + Vite) and the mobile app (React Native + Expo). Samuel's two frontends will hit the same endpoints — you don't write separate endpoints for mobile. Your API is the single source of truth for all data.

---

## What You Are Responsible For

- Setting up and maintaining the Django project structure
- Designing and managing all database models (Rooms, Bookings, Users)
- Writing all REST API endpoints that Samuel's frontend and mobile app will consume
- Handling user registration, login, and authentication
- Writing business logic — for example, checking if a room is already booked before confirming a new booking
- Handling image/file uploads for room photos
- Writing admin-only endpoints so the hotel manager can manage rooms and bookings
- Configuring CORS so Samuel's frontend can communicate with your server without browser errors
- Deploying the API to a live server when the project is ready

---

## Project Structure

Your Django backend sits inside the `backend/` folder of the shared repository. Inside it, you will have:

- `core/` — the main Django project folder (holds `settings.py`, `urls.py`, etc.)
- `rooms/` — the app that manages room data
- `bookings/` — the app that manages booking records
- `users/` — the app that handles authentication and user profiles
- `manage.py` — Django's command-line tool
- `requirements.txt` — list of all Python packages Samuel or another developer needs to install

Each app follows Django's standard structure: `models.py`, `serializers.py`, `views.py`, `urls.py`.

---

## Day-by-Day Build Plan

---

### Day 1 — Project Setup

**Goal:** Get the Django server running and connected to PostgreSQL. Samuel cannot test anything without CORS being enabled, so this must be done on Day 1.

**What to do:**

1. Create the Django project using `django-admin startproject core .` from inside the `backend/` folder.
2. Create three apps: `rooms`, `bookings`, and `users`.
3. Install all required packages:
   - `djangorestframework` — this is what turns Django into an API server
   - `django-cors-headers` — this allows Samuel's frontend (running on port 5173) to talk to your server (running on port 8000) without the browser blocking it
   - `Pillow` — required for Django to handle image uploads
   - `python-decouple` — lets you store sensitive config (like your database password) in a `.env` file instead of hardcoding it
   - `psycopg2-binary` — the driver that allows Django to talk to PostgreSQL
4. Set up `settings.py`:
   - Connect PostgreSQL as your database
   - Add `corsheaders` to `INSTALLED_APPS` and `MIDDLEWARE`
   - Set `CORS_ALLOWED_ORIGINS` to include `http://localhost:5173` (Samuel's dev server)
5. Create a `.env` file with your `SECRET_KEY`, database name, database user, database password, host, and port. Never commit this file to GitHub.
6. Push your initial setup to your branch (`victor/backend`).

**Deliverable:** Running `python manage.py runserver` starts the server on `localhost:8000` without errors.

**Tell Samuel:** CORS is enabled. He can now make requests from his frontend.

---

### Day 2 — Room Model and API

**Goal:** Build the Room model and expose two public endpoints so Samuel can fetch room data.

**What to do:**

1. In `rooms/models.py`, create a `Room` model with the following fields:
   - `name` — the room's display name (e.g., "Deluxe Suite")
   - `room_type` — one of three options: `suite`, `apartment`, or `basic`
   - `description` — a longer text description of the room
   - `price_per_night` — stored as a decimal number with two decimal places
   - `capacity` — maximum number of guests allowed
   - `image` — the uploaded room photo, stored in a subfolder of your `media/` directory
   - `is_available` — a true/false flag that defaults to `True`
   - `amenities` — a JSON list of features (e.g., `["WiFi", "Air Conditioning", "TV"]`)
   - `created_at` — automatically set to the timestamp when the record is created

2. Run migrations to create the database table.

3. In `rooms/serializers.py`, create a `RoomSerializer`. A serializer converts your Django model instance into JSON so the API can send it to Samuel's frontend. Pay attention to the `image` field — it must return a full URL (e.g., `http://localhost:8000/media/rooms/photo.jpg`), not just a file path. Use `serializers.ImageField(use_url=True)` to ensure this.

4. Create two views:
   - A list view that returns all rooms
   - A detail view that returns a single room by its ID

5. Wire up the URLs:
   - `GET /api/rooms/` → returns all rooms
   - `GET /api/rooms/:id/` → returns one room's full details

6. Add at least a few sample rooms via the Django Admin panel so Samuel has real data to work with.

**Deliverable:** Samuel can visit `http://localhost:8000/api/rooms/` and see room data in JSON format.

---

### Day 3 — User Authentication

**Goal:** Allow guests to register and log in. Protect endpoints that require a logged-in user.

**What to do:**

1. In `users/models.py`, extend Django's built-in `AbstractUser` model. This gives you everything Django's default user has (email, password, etc.) plus your custom fields:
   - `phone_number` — optional contact number
   - `role` — either `guest` or `admin`, to distinguish regular users from hotel staff

2. Choose an authentication method — **JWT is recommended** for this project because it works cleanly for both web and mobile:
   - Install `djangorestframework-simplejwt`
   - JWT works like this: when a user logs in, they get two tokens — an **access token** (short-lived, used to make authenticated requests) and a **refresh token** (long-lived, used to get a new access token without logging in again)
   - Samuel stores these tokens in his frontend and sends the access token in the request header for any protected endpoint

3. Create three endpoints:
   - `POST /api/auth/register/` — accepts a name, email, and password, creates a new user, and returns tokens
   - `POST /api/auth/login/` — accepts email and password, validates them, and returns access + refresh tokens
   - `POST /api/auth/logout/` — invalidates the refresh token (requires auth)

4. For any endpoint that requires a logged-in user, add the `IsAuthenticated` permission class to the view.

**Deliverable:** A user can register, log in, and receive a token. Samuel knows to send `Authorization: Bearer <access_token>` in the request header.

**Tell Samuel immediately:** Which auth method you chose and exactly what header format he needs to use.

---

### Day 4 — Booking Model and API

**Goal:** Let authenticated guests submit bookings and view their own booking history.

**What to do:**

1. In `bookings/models.py`, create a `Booking` model:
   - `user` — a ForeignKey to your User model (who made the booking)
   - `room` — a ForeignKey to the Room model (which room is being booked)
   - `check_in` — the date the guest arrives
   - `check_out` — the date the guest leaves
   - `guests` — number of guests in the booking
   - `total_price` — calculated automatically from the room's `price_per_night` multiplied by the number of nights
   - `status` — one of four states: `pending`, `confirmed`, `checked_out`, or `cancelled`
   - `created_at` — timestamp of when the booking was submitted

2. Run migrations.

3. Create a `BookingSerializer`.

4. Create the following views — all require authentication (`IsAuthenticated`):
   - `POST /api/bookings/` — creates a new booking
   - `GET /api/bookings/` — returns only the logged-in user's bookings (not everyone's)
   - `GET /api/bookings/:id/` — returns the detail of one specific booking

5. **Availability check logic** — this is critical business logic. Before saving a new booking, your view must check: does another confirmed or pending booking already exist for that room that overlaps with the requested dates? If yes, return a `400 Bad Request` error with a clear message. A date overlap exists when the requested `check_in` is before an existing `check_out` AND the requested `check_out` is after an existing `check_in`.

6. **Total price calculation** — in the serializer or view, calculate `total_price` automatically as: `(check_out - check_in).days × room.price_per_night`. Never trust the frontend to send this value.

**Deliverable:** Samuel's booking form can submit to this endpoint and the user can see their bookings on the profile/bookings page.

---

### Day 5 — Admin Endpoints

**Goal:** Give hotel staff the ability to manage rooms and all bookings through the API.

**What to do:**

1. Create a set of admin-only endpoints. These views must be protected with Django's `IsAdminUser` permission class, which only allows users where `is_staff=True`. No regular guest should ever be able to hit these.

2. Admin booking endpoints:
   - `GET /api/admin/bookings/` — returns all bookings from all users
   - `PUT /api/admin/bookings/:id/` — update a booking's status (e.g., change from `pending` to `confirmed`)

3. Admin room endpoints:
   - `GET /api/admin/rooms/` — list all rooms
   - `POST /api/admin/rooms/` — add a new room (with image upload)
   - `PUT /api/admin/rooms/:id/` — edit an existing room's details
   - `DELETE /api/admin/rooms/:id/` — remove a room

4. Create a superuser using `python manage.py createsuperuser` for testing.

**Deliverable:** The hotel admin can manage all rooms and update booking statuses. Samuel can build the admin dashboard UI that calls these endpoints.

---

### Day 6 — Image Uploads and Media Files

**Goal:** Allow room images to be uploaded, stored, and served correctly.

**What to do:**

1. In `settings.py`, set two values:
   - `MEDIA_URL` — the URL prefix for serving media files (e.g., `/media/`)
   - `MEDIA_ROOT` — the actual folder on disk where files are saved (e.g., `BASE_DIR / 'media'`)

2. In your main `urls.py`, add the static file serving route for development. This tells Django to serve files from `MEDIA_ROOT` when a URL starting with `MEDIA_URL` is requested. This is only for development — on production, your server (Nginx/Render/Railway) handles this.

3. Verify that when you upload a room image through the API, the returned JSON contains the full image URL (e.g., `http://localhost:8000/media/rooms/room1.jpg`) and not just the filename.

4. Test this end-to-end — upload an image, copy the URL from the JSON response, paste it in the browser, and confirm the image loads.

**Important note for production:** When you deploy, images stored locally will be lost unless you use a dedicated file storage service. Consider using Cloudinary or AWS S3 with `django-storages` for persistent image storage in production. Flag this to Samuel early.

**Deliverable:** Room images upload successfully and Samuel can display them on the frontend using the URL returned from the API.

---

### Day 7 — Contact Form Endpoint (Optional)

**Goal:** Capture messages sent through Samuel's contact page.

**What to do:**

1. Create a `Contact` model with: `name`, `email`, `message`, and `created_at`.
2. Expose one endpoint: `POST /api/contact/` — no authentication required.
3. Optionally, use Django's built-in `send_mail()` function to forward the message to the hotel's email address.
4. Return a success response so Samuel can show a confirmation message to the user.

**Deliverable:** Contact form submissions are saved to the database and optionally emailed to the hotel.

---

### Day 8 — Testing and Cleanup

**Goal:** Make the API stable, predictable, and error-safe before deployment.

**What to do:**

1. Test every endpoint thoroughly using Postman or the DRF Browsable API. Test both happy paths (valid input) and unhappy paths (missing fields, wrong auth, booking conflicts).

2. Add proper HTTP error responses:
   - `400 Bad Request` — for invalid input (e.g., missing required fields, date conflicts)
   - `401 Unauthorized` — for requests made without a valid token
   - `403 Forbidden` — for guests trying to access admin endpoints
   - `404 Not Found` — for requests for rooms or bookings that don't exist

3. Add pagination to list endpoints. Without this, if there are 500 bookings, the API returns all 500 at once. Use DRF's `PageNumberPagination` to return a manageable page size (e.g., 10 or 20 per page). Tell Samuel the pagination format so his frontend can handle the `next` and `previous` links.

4. Add filtering and search to the rooms endpoint:
   - `GET /api/rooms/?type=suite` — filter by room type
   - `GET /api/rooms/?available=true` — filter by availability
   This lets Samuel build filter/search functionality on the rooms listing page.

5. Write at least basic automated tests for your models and views using Django's built-in test runner (`python manage.py test`).

**Deliverable:** The API handles edge cases gracefully and does not crash on bad input.

---

### Day 9 — Deployment

**Goal:** Get the API live so both Samuel's deployed web app and the mobile app can reach it.

**What to do:**

1. Install production dependencies:
   - `gunicorn` — a production-grade server that runs Django (replaces `python manage.py runserver`)
   - `whitenoise` — serves Django's static files without needing a separate web server config

2. Update `settings.py` for production:
   - Set `DEBUG = False`
   - Add your production domain to `ALLOWED_HOSTS`
   - Configure `STATIC_ROOT` and run `collectstatic`
   - Load all secrets from environment variables — never hardcode them

3. Deploy to your chosen platform (Railway or Render are both good free-tier options). Render's free tier is a good starting point.

4. Update `CORS_ALLOWED_ORIGINS` to include Samuel's deployed frontend URL.

5. Update Samuel's `api.js` with your live API base URL.

6. For mobile: Samuel's phone cannot use `localhost`. During development, he uses your local IP address (e.g., `192.168.x.x:8000`). After deployment, he updates to the live URL. Ensure your `ALLOWED_HOSTS` includes both `localhost` and your production domain.

**Deliverable:** The API is live. Samuel's deployed web app and his mobile app both successfully communicate with it.

---

## Data Models Reference

### Room Model (`rooms` app)

| Field | Type | Notes |
|---|---|---|
| `id` | Auto | Primary key, auto-generated |
| `name` | CharField | e.g., "Ocean Suite" |
| `room_type` | CharField | One of: `suite`, `apartment`, `basic` |
| `description` | TextField | Long description of the room |
| `price_per_night` | DecimalField | Use 2 decimal places |
| `capacity` | IntegerField | Maximum number of guests |
| `image` | ImageField | Stored in `media/rooms/` |
| `is_available` | BooleanField | Defaults to `True` |
| `amenities` | JSONField | List of strings, e.g., `["WiFi", "Pool"]` |
| `created_at` | DateTimeField | Auto-set on creation |

---

### Booking Model (`bookings` app)

| Field | Type | Notes |
|---|---|---|
| `id` | Auto | Primary key |
| `user` | ForeignKey | Links to the User who made the booking |
| `room` | ForeignKey | Links to the Room being booked |
| `check_in` | DateField | Arrival date |
| `check_out` | DateField | Departure date |
| `guests` | IntegerField | Number of guests in party |
| `total_price` | DecimalField | Calculated server-side, never from frontend |
| `status` | CharField | One of: `pending`, `confirmed`, `checked_out`, `cancelled` |
| `created_at` | DateTimeField | Auto-set on creation |

---

### User Model (`users` app)

| Field | Type | Notes |
|---|---|---|
| Inherits all fields from Django's `AbstractUser` | — | email, password, first_name, etc. |
| `phone_number` | CharField | Optional |
| `role` | CharField | Either `guest` or `admin` |

---

## Full API Endpoints Reference

| Method | Endpoint | Auth Required | Who Uses It | Description |
|---|---|---|---|---|
| GET | `/api/rooms/` | No | Samuel (web + mobile) | List all rooms |
| GET | `/api/rooms/:id/` | No | Samuel (web + mobile) | Single room detail |
| POST | `/api/auth/register/` | No | Samuel | Guest registration |
| POST | `/api/auth/login/` | No | Samuel | Login, returns JWT tokens |
| POST | `/api/auth/logout/` | Yes (Guest) | Samuel | Logout, invalidates token |
| POST | `/api/bookings/` | Yes (Guest) | Samuel | Submit a new booking |
| GET | `/api/bookings/` | Yes (Guest) | Samuel | User's own booking history |
| GET | `/api/bookings/:id/` | Yes (Guest) | Samuel | Single booking detail |
| POST | `/api/contact/` | No | Samuel | Contact form submission |
| GET | `/api/admin/bookings/` | Yes (Admin) | Samuel (admin dashboard) | All bookings from all users |
| PUT | `/api/admin/bookings/:id/` | Yes (Admin) | Samuel (admin dashboard) | Update booking status |
| GET | `/api/admin/rooms/` | Yes (Admin) | Samuel (admin dashboard) | All rooms |
| POST | `/api/admin/rooms/` | Yes (Admin) | Samuel (admin dashboard) | Add a new room |
| PUT | `/api/admin/rooms/:id/` | Yes (Admin) | Samuel (admin dashboard) | Edit a room |
| DELETE | `/api/admin/rooms/:id/` | Yes (Admin) | Samuel (admin dashboard) | Delete a room |

---

## Communication Checklist with Samuel

These are things you must tell Samuel at specific points so he is not blocked:

- **Day 1** — Tell him CORS is enabled and he can start making requests from his frontend.
- **Day 2** — Tell him the rooms endpoint is live. Share the exact URL and a sample JSON response so he knows the shape of the data.
- **Day 3** — Tell him which auth method you chose (JWT), the exact token format, and the header he must send: `Authorization: Bearer <access_token>`. Also tell him what fields `register` and `login` expect in the request body.
- **Day 4** — Tell him the bookings endpoint is live. Tell him which fields are required in the POST body and what the error response looks like for a date conflict.
- **Day 5** — Tell him the admin endpoints are live so he can wire up the admin dashboard.
- **Day 9** — Share the live production API URL so he can update both the web app and the mobile app.

---

## Important Technical Notes

### Multipart vs JSON requests
Some endpoints accept images (room creation/update) — these must use `multipart/form-data` encoding, not `application/json`. Tell Samuel this distinction clearly. Endpoints that don't involve file uploads can use standard JSON.

### Never trust the frontend for calculated values
Always calculate `total_price` on the server using the room's price and the date range. If Samuel sends a `total_price` in the request body, ignore it.

### Image URLs must be absolute
Always return full URLs for image fields in your serializers (e.g., `http://localhost:8000/media/rooms/photo.jpg`), not relative paths. Samuel's frontend needs the full URL to display images.

### Mobile network access
Samuel's phone cannot reach `localhost`. During local development, replace `localhost` with your machine's local network IP (e.g., `192.168.1.x`) in `ALLOWED_HOSTS` and tell Samuel to update his mobile `api.js` accordingly.

### Keep `requirements.txt` updated
Every time you install a new package, run `pip freeze > requirements.txt` and commit it. This ensures anyone cloning the repo can install all dependencies in one command.

### Environment variables
Never hardcode secrets. Everything sensitive goes in `.env` and is read using `python-decouple`. Add `.env` to `.gitignore`. Provide a `.env.example` file with placeholder values for Samuel and any future developer.

---

## Glossary

| Term | What it means in plain English |
|---|---|
| **Serializer** | A translator between Python objects (your Django models) and JSON (what the API sends and receives) |
| **Migration** | A file Django generates that describes changes to your database structure. Running it actually applies those changes to the database |
| **CORS** | A browser security rule that blocks requests from one domain (Samuel's React app) to another (your API) unless you explicitly allow it |
| **JWT** | JSON Web Token. A small, signed string that proves a user is logged in. Comes in two parts: access token (short-lived) and refresh token (long-lived) |
| **Permission class** | A DRF tool that decides who is allowed to use a particular API view. Examples: `IsAuthenticated`, `IsAdminUser` |
| **ForeignKey** | A database relationship. In a Booking, the `user` ForeignKey means "this booking belongs to that user" |
| **AbstractUser** | Django's base user class. Extending it means you get all of Django's built-in user features plus your own custom fields |
| **Gunicorn** | A production server for running Django. Unlike `runserver`, it is designed for real traffic |
| **Whitenoise** | A Python package that lets Django serve its own static files in production without a separate web server |
| **Pagination** | Splitting large lists of results into pages instead of returning everything at once |