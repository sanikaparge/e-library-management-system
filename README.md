# E-Library Management System

Simple elegant library management project with subtle animation.

## Features
- 20 starter books in 4 categories
- Search and category filtering
- Add books
- Create memberships and store member details
- Issue and return books
- Issue history and dashboard statistics

## Stack
HTML5, CSS3, JavaScript, Python, Flask, Flask-SQLAlchemy, PostgreSQL, Docker, Docker Compose, Git/GitHub, AWS EC2.

## Local run
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python backend\app.py
```
Open http://127.0.0.1:5000

## Docker
```bash
docker compose up --build
```


## UI & Validation Upgrade
- Live book search across title, author, category and ISBN
- Working category filters with combined search + category filtering
- Exact 10-digit Indian mobile-number validation on frontend and backend
- Improved responsive layout and accessibility labels
- More polished micro-interactions, reveal animations, hover states and transitions
- Reduced-motion support for accessibility
