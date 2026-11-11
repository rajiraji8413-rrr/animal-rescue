# 🐾 Animal Rescue – Django Web Application

## 📌 Project Overview

Animal Rescue is a web-based application developed using Python and Django. It helps users explore animals available for adoption, view animal details, submit adoption requests and manage their rescue activities.

The application provides an organized platform to connect animals in need of homes with potential adopters.

## 🚀 Features

- **Animal Listings:** Display available animals for adoption.
- **Animal Details:** View animal information, descriptions and photos.
- **Search and Filtering:** Search and filter animals based on available criteria.
- **User Authentication:** User registration, login and logout.
- **User Profile:** Manage user profile information.
- **Adoption Requests:** Submit and track adoption requests.
- **Admin Dashboard:** Manage animal listings and application data.
- **Image Management:** Display animal photos.
- **Responsive Interface:** User-friendly website interface.

## 🛠️ Technologies Used

**Backend**
- Python
- Django

**Frontend**
- HTML5
- CSS3
- Bootstrap
- JavaScript

**Database**
- PostgreSQL

**Tools**
- Visual Studio Code
- Git
- GitHub

**Deployment**
- Render

## 📂 Project Structure

```text
animal_rescue/
│
├── animals/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── forms.py
│
├── templates/
├── static/
├── media/
├── animal_rescue/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd animal_rescue
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Configure your database credentials and Django secret key in your environment variables.

Do not commit secret keys or API credentials to GitHub.

### 7. Apply Migrations

```bash
python manage.py migrate
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

Open your browser:

```text
http://127.0.0.1:8000/
```

## 🌐 Deployment

The application has been successfully deployed using Render.

**Live Demo:** Add your deployed application URL here.

## 🔮 Future Enhancements

- Integrate RescueGroups REST API for external animal adoption listings.
- Display live animal adoption data from external sources.
- Add location-based animal searches.
- Implement adoption status notifications.
- Improve adoption application management.

## 👩‍💻 Developer

Developed as a Python and Django web development project.

**Project:** Animal Rescue Management System

**Backend:** Python | Django

---

⭐ If you find this project useful, feel free to explore the repository!
