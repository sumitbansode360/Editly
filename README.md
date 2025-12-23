# ✍️ Editly – Real-Time Collaborative Document Editor

Editly is a Django-powered web application that enables multiple users to collaboratively create, edit, and manage documents in real time. It demonstrates live document editing similar to Google Docs using WebSockets and Django Channels, along with secure authentication and document search functionality.

This project focuses on real-time communication, backend-heavy architecture, and practical Django concepts used in production systems.

---

## 🚀 Features

### 🔐 User Authentication
- User registration & login  
- Secure access to documents  

### 📝 Real-Time Collaborative Editing
- Multiple users can edit the same document simultaneously  
- Changes are reflected live using WebSockets  
- Powered by Django Channels  

### 📄 Document Management
- Create, edit, and delete documents  
- Ownership-based access control  

### 🔍 Search Functionality
- Search documents by title/content  
- Fast and user-friendly filtering  

### ⚡ Live Updates
- No page refresh required  
- WebSocket-based communication  

### 🎨 Responsive UI
- Built using Bootstrap  
- Simple and clean interface  

---

## 🛠 Tech Stack

### Backend
- Django  
- Django Channels  
- WebSockets  
- SQLite (can be upgraded to PostgreSQL)  

### Frontend
- HTML  
- CSS  
- Bootstrap  
- JavaScript  

### Other
- Redis (for Channels layer, if used)  
- Django Auth System  

---

## 🧠 Architecture Overview

- **HTTP** → Used for authentication, document creation, and fetching data  
- **WebSockets** → Used for real-time document editing  
- **Channels Layer** → Manages communication between users editing the same document  
- **Consumers** → Handle real-time events and broadcasting updates  

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/editly.git
cd editly

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser

6. Start the Server
python manage.py runserver

