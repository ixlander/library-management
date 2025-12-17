
# 📚 Library Management System

A full-stack web application for managing books and manga collections. Users can register, browse titles, leave reviews, mark favorites, and track their reading journey.

---

## 👨‍💻 Authors

- **Abakarov Maxim**
- **Beisen Abylai**
- **Kumar Aray**

---

## ⚙️ Tech Stack

### 💻 Frontend

- Angular
- TypeScript
- SCSS / HTML
- Angular Router
- JWT Authentication

### 🛠 Backend

- Django & Django REST Framework
- SQLite (or PostgreSQL)
- JWT (via `djangorestframework-simplejwt`)
- CORS Support (`django-cors-headers`)

---

## 🚀 Features

- ✅ User registration and JWT-based login
- ✅ Browse and search books/manga
- ✅ Leave reviews and ratings
- ✅ Add items to favorites
- ✅ Track reading progress

---

## 🧰 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ixlander/library-management.git
cd library-management
```

### 2️⃣ Backend Setup (Django)

```bash
cd library_backend

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install django
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

### 3️⃣ Frontend Setup (Angular)

```bash
cd ../frontend

# Install Angular dependencies
npm install

# Run Angular development server
ng serve
```

---

## 🔃 Development Workflow

- Work on features in `dev` branch
- Test and merge to `main` after validation

```bash
git checkout dev
git pull origin dev
```

---

## 📜 License

Licensed under the MIT License.
