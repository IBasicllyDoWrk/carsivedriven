# 🚗 Cars I've Driven

Welcome to **Cars I've Driven** — a simple yet stylish Flask web app that lets you log, edit, and reflect on every car you've ever driven. Whether you're a car enthusiast, a curious road-tripper, or just someone with a long rental history, this app is built for you.

---

## 📋 Features

- 🔐 Secure user registration and login
- 🚘 Add/edit/delete cars with details like make, model, year, engine, and transmission
- 📊 Dashboard view of all cars driven
- 📈 Profile page with fun stats: total cars, oldest, newest
- 🛠️ Update or delete your profile
- 🎨 Clean, responsive UI (Bootstrap + custom CSS)
- 🧼 CSRF protection, rate limiting, and hashed passwords for safety

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/carsivedriven.git
cd carsivedriven
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# Activate:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set the Secret Key (Optional but Recommended)
Create a `.env` file in the root directory:

```env
SECRET_KEY=your_super_secret_key
```

You can also export it directly:
```bash
export SECRET_KEY=your_super_secret_key
```

### 5. Initialize the Database
```bash
python
>>> from app import init_db
>>> init_db()
>>> exit()
```

### 6. Run the App
```bash
flask run
```

---

## 🗃️ Project Structure

```
carsivedriven/
│
├── static/               # CSS and images
├── templates/            # HTML templates
├── app.py                # Main Flask app
├── forms.py              # WTForms definitions
├── database.db           # SQLite database (gitignored)
├── requirements.txt      # Python dependencies
├── .gitignore            # Files to ignore in Git
└── README.md             # This file
```

---

## 📷 Screenshots

[Dashboard Preview]  
[Add Car Form]  
[User Profile View]

---

## ⚙️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: SQLite
- **Forms**: Flask-WTF (CSRF-protected)
- **Security**: Werkzeug (password hashing), Flask-Limiter

---

## 💡 Future Ideas

- ✅ Dark mode toggle
- 📈 Stats page with charts
- 🌐 Export cars to CSV
- 🖼️ Add car images

---

## 📝 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

Built with caffeine, curiosity, and a love for anything on four wheels.  
If you enjoy using it, consider giving this repo a ⭐️!

---

> _“It’s not just about the cars you’ve driven. It’s about the stories behind the steering wheels.”_
