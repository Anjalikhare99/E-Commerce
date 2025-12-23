![Work in Progress](https://img.shields.io/badge/status-WIP-orange)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-4.2-green)

# E-Commerce Application (Work in Progress)

This is a Django-based E-Commerce application under development.  
It will allow users to browse products, register/login, and manage orders.

---

## 🚀 Planned Features
- User authentication (Signup/Login/Logout)
- Product listing with categories and subcategories
- Product detail page with images and descriptions
- Cart and checkout system
- Admin panel for managing products, orders, and users
- Role-based access (Admin/Seller/Customer)
- Order history and tracking
- Search and filter functionality

---

## 🛠️ Tech Stack
- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (can be upgraded to PostgreSQL/MySQL)
- **Tools:** Git, GitHub
- **Planned:** Django REST Framework (for API), Celery, Docker, AWS deployment

---

## 📂 Project Structure (Planned)
E-Commerce/
├── E-Commerce/ # Main Django project
├── account/ # User authentication & accounts
├── seller/ # Seller app for managing products
├── templates/ # HTML templates
├── static/ # CSS, JS, images
├── db.sqlite3
├── manage.py
└── requirements.txt

---

# Clone repository
git clone https://github.com/Anjalikhare99/E-Commerce.git

# Navigate to project directory
cd E-Commerce

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

