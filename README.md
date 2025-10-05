# Guess The Word 🎮

A **Flask-based web game** where players guess 5-letter words, similar to Wordle. Includes **player and admin functionalities**, daily and user-specific reports, and an attractive, interactive frontend.

---

## Table of Contents

- [Features](#features)  
- [Demo](#demo)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Admin Reports](#admin-reports)  
- [Tech Stack](#tech-stack)  
- [Folder Structure](#folder-structure)  
- [Future Enhancements](#future-enhancements)  

---

## Features

### Player
- User registration and login with validation.
- Play **Guess the Word** game (5 guesses per game).  
- Visual feedback on guesses:
  - Green = correct letter & position  
  - Orange = correct letter, wrong position  
  - Grey = wrong letter
- Flash messages with **color-coded feedback**:
  - Correct guess → Green  
  - Incorrect guess → Orange
- Previous guesses are displayed with colored letters.
- Daily game limit: 3 games per user.

### Admin
- Admin login to access **dashboard**.
- **Daily Report**: Number of users who played and number of correct guesses.  
- **User Report**: For a specific user:
  - Date of games  
  - Number of words tried  
  - Number of correct guesses
- User-friendly tables and interactive interface.

---


## Installation

### 1️⃣ Clone the repository

```bash
git clone <your-github-repo-url>
cd Guess_The_Word

2️⃣ Create a virtual environment
python -m venv venv

3️⃣ Activate the virtual environment

Windows:
venv\Scripts\activate


Mac/Linux:
source venv/bin/activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the app
python run.py


Open in browser: http://127.0.0.1:5000

Usage :

Register / Login
Register a new account or login with existing credentials.
Admin accounts must be manually promoted in the database (is_admin=True).

Playing the Game :

Enter 5-letter words to guess.
Previous guesses are displayed with colors.
Maximum 5 guesses per game.
Maximum 3 games per day.

Admin Reports :

Navigate to /admin/daily for the daily report.
Navigate to /admin/user to search and view reports for a specific user.

Tech Stack :

Backend: Python, Flask
Frontend: HTML, CSS, JavaScript
Database: SQLite 
Authentication: Flask-Login
Version Control: Git & GitHub

Folder Structure :

Guess_The_Word/
├─ app/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ routes/
│  │  ├─ auth.py
│  │  ├─ game.py
│  │  └─ admin.py
│  └─ utils.py
├─ static/
│  ├─ css/style.css
│  └─ js/main.js
├─ templates/
│  ├─ login.html
│  ├─ register.html
│  ├─ game.html
│  └─ admin.html
|     home.html
├─ database/
│  └─ guess_game.db
├─ venv/
├─ requirements.txt


Future Enhancements:

Deploy to Render or Railway for online access.
Replace SQLite with PostgreSQL for scalability.
Add leaderboard for daily top players.
Add word categories and difficulty levels.
Improve mobile responsiveness and animations.