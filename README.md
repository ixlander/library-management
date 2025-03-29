# 📚 Library Management System (Books & Manga)

## 📖 About the Project
**Library Management System** is a web application designed for managing books and manga. Users can browse available books, leave reviews, add favorites, and track their reading progress.

## 🔧 Technologies

### Frontend:
- Angular
- TypeScript
- HTML, SCSS
- Angular Router
- JWT Authentication

### Backend:
- Django + Django REST Framework
- PostgreSQL (or SQLite)
- JWT Authentication
- DRF Serializers & Views

## 🚀 Features
✔ User registration & authentication (JWT)  
✔ Browse book & manga catalog  
✔ Leave reviews and ratings  
✔ Add books to favorites  
✔ Track reading progress  
✔ Search and filter books  

## 🔧 Installation & Setup

### 📦 Clone the Repository
```bash
git clone https://github.com/ixlander/library-management.git
cd library-management
```

### 🔥 Backend (Django)
1. Navigate to the `backend` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```

### 🎨 Frontend (Angular)
1. Navigate to the `frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the local development server:
   ```bash
   ng serve
   ```

## 🛠 Development Workflow

### Branching Strategy
- The main development happens in the `dev` branch.
- New features should be developed in `feature/your-feature-name` branches.
- After testing, the code is merged into `dev`, then into `main`.

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

## 📜 License
MIT License
