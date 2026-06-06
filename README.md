# Buena Vista Cottage — Hotel Website

A modern, full-stack hotel platform for **Buena Vista Cottage**, a boutique Nigerian hotel. Built with React (Vite) on the frontend, React Native (Expo) for the mobile app, and Django on the backend, featuring immersive 3D animations, room booking, and a clean admin experience.

---

## Features

- **3D Animations & Transitions** — Smooth, immersive UI powered by Framer Motion
- **Room Showcase** — Browse Suite, Apartment, and Basic room types with interactive cards
- **Room Booking** — Real-time availability checking and booking submission
- **Authentication** — Guest login/signup and admin access
- **Fully Responsive** — Optimized for mobile, tablet, and desktop
- **Admin Dashboard** — Manage rooms, bookings, and guests
- **Mobile App** — React Native (Expo) app sharing the same Django API

---

## Tech Stack

### Frontend
| Tool | Purpose |
|------|---------|
| React + Vite | UI framework & dev server |
| React Router DOM | Client-side routing |
| Framer Motion | 3D animations & transitions |
| Axios | API communication |
| React Icons | Icon library |
| React Hot Toast | Notifications |

### Backend
| Tool | Purpose |
|------|---------|
| Django | Web framework |
| Django REST Framework | API layer |
| django-cors-headers | Cross-origin support |
| PostgreSQL | Database |

### Mobile
| Tool | Purpose |
|------|---------|
| React Native + Expo | Mobile app framework |
| React Navigation | Screen routing |
| Axios | API communication (same Django API) |
| Expo Go | Dev preview on physical device |

---

## Project Structure

```
buena-vista-cottage/
├── frontend/                  # React + Vite app
│   ├── public/
│   │   └── images/            # Hotel & room photos
│   ├── src/
│   │   ├── assets/            # Fonts, icons
│   │   ├── components/        # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── RoomCard.jsx
│   │   │   └── BookingForm.jsx
│   │   ├── pages/             # Route-level pages
│   │   │   ├── Home.jsx
│   │   │   ├── Rooms.jsx
│   │   │   ├── RoomDetail.jsx
│   │   │   ├── Booking.jsx
│   │   │   ├── About.jsx
│   │   │   └── Contact.jsx
│   │   ├── services/          # Axios API calls
│   │   │   └── api.js
│   │   ├── context/           # Auth & booking context
│   │   ├── hooks/             # Custom React hooks
│   │   ├── utils/             # Helper functions
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env
│   └── package.json
│
└── backend/                   # Django app
    ├── hotel/                 # Core app
    ├── bookings/              # Bookings app
    ├── users/                 # Auth app
    ├── manage.py
    └── requirements.txt

mobile/                        # React Native + Expo app
├── app/
│   ├── screens/               # One file per screen
│   │   ├── HomeScreen.jsx
│   │   ├── RoomsScreen.jsx
│   │   ├── RoomDetailScreen.jsx
│   │   ├── BookingScreen.jsx
│   │   └── ProfileScreen.jsx
│   ├── components/            # Reusable mobile components
│   ├── services/              # Same API calls as web
│   │   └── api.js
│   └── context/               # Auth context
├── app.json
└── package.json
```

---

## Getting Started

### Prerequisites

- Node.js v18+
- Python 3.10+
- PostgreSQL

---

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Set VITE_API_BASE_URL=http://localhost:8000/api

# Start dev server
npm run dev
```

App runs at **http://localhost:5173**

---

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in DB credentials, SECRET_KEY, etc.

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

API runs at **http://localhost:8000/api**

---

### Mobile Setup

```bash
# Navigate to mobile
cd mobile

# Install dependencies
npm install

# Start Expo dev server
npx expo start
```

Scan the QR code with the **Expo Go** app on your phone to preview instantly.

The mobile app connects to the same Django API — just make sure the backend is running and update `api.js` with your local IP address instead of `localhost` (e.g. `http://192.168.x.x:8000/api`) so your phone can reach it.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/rooms/` | List all rooms |
| `GET` | `/api/rooms/:id/` | Room detail |
| `POST` | `/api/bookings/` | Create a booking |
| `GET` | `/api/bookings/` | List bookings (admin) |
| `POST` | `/api/auth/register/` | Guest registration |
| `POST` | `/api/auth/login/` | Guest login |
| `POST` | `/api/auth/logout/` | Logout |

---

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero section, highlights, CTA |
| Rooms | `/rooms` | All room types with 3D cards |
| Room Detail | `/rooms/:id` | Full room info & booking form |
| About | `/about` | Hotel story and amenities |
| Contact | `/contact` | Contact form & map |
| Admin | `/admin` | Booking & room management |

---

## Environment Variables

### Frontend (`.env`)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Backend (`.env`)
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/buena_vista
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

---

## Team

| Role | Name | Responsibility |
|------|------|---------------|
| Frontend (Web) | Samuel | React UI, animations, routing |
| Mobile | Samuel | React Native screens, Expo setup |
| Backend | Victor | Django API, database, auth |

---

## License

This project is private and built for **Buena Vista Cottage**. All rights reserved.