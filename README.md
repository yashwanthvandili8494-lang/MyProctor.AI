# 🎓 MyProctor.ai — AI-Based Smart Online Examination & Proctoring System

<p align="center">
  <img src="https://assets1.lottiefiles.com/packages/lf20_wEt2nn.json" width="120" alt="MyProctor Logo" />
</p>

<p align="center">
  <b>An intelligent, automated online examination platform with real-time AI-driven proctoring, live violation tracking, and multi-format exam support.</b>
</p>

<p align="center">
  <a href="https://portfolio-jade-one-1cqukhqrqd.vercel.app/"><img src="https://img.shields.io/badge/Author-Yashvant-blue?style=for-the-badge&logo=vercel" alt="Author Yashvant" /></a>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask" alt="Flask" />
  <img src="https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL-003B57?style=for-the-badge&logo=sqlite" alt="Database" />
</p>

---

## 📌 Project Overview

**MyProctor.ai** is an end-to-end smart examination and invigilation platform engineered to ensure academic integrity in remote online exams. Powered by computer vision and machine learning models, the system continuously analyzes student video and behavioral metrics to flag suspicious activities in real time.

---

## ✨ Key Features

### 🛡️ 1. AI Proctoring & Anti-Cheating Engine
- **Face Authentication**: Verified image capture at login and continuous facial verification during exams.
- **Multiple Person Detection**: Detects if more than one individual appears in the camera frame.
- **Mobile Phone / Object Detection**: Identifies unauthorized handheld devices.
- **Gaze & Head Pose Tracking**: Monitors student attention, flagging excessive head or eye deviations.
- **Audio Frequency Monitoring**: Samples ambient audio at 5-second intervals to detect voices or whispered communication.
- **Window & Tab Switch Tracker**: Records every unfocus, window switch, or tab change event.
- **Lockdown Security**: Disables right-click, cut, copy, paste, and screenshot shortcuts.

### 📝 2. Multi-Format Exam Support
- **Objective Exams (MCQ)**:
  - Single-question paging with intuitive question grid navigation.
  - Bookmark & review options before final submission.
  - Negative marking configuration and question randomization.
- **Subjective Exams**:
  - Essay & descriptive answer submission with word tracking.
- **Practical (Coding) Exams**:
  - In-browser code editor with multi-language compiler & interpreter integration.
  - Support for 20+ programming languages.

### 👨‍🏫 3. Professor Portal
- **AI Question Generator**: Automatically generate objective and subjective questions.
- **Exam Management**: Create, schedule, update, or archive exams with custom timers.
- **Live Exam Monitoring**: Real-time dashboard showing connected students and live violation alerts.
- **Student Audit Logs**: Detailed timeline of window events, audio anomalies, and captured webcam snapshots.
- **Grading & Result Publishing**: Seamless scoring for subjective & practical submissions with one-click result publishing.

### 👨‍🎓 4. Student Portal
- **Student Dashboard**: Overview of assigned exams, upcoming schedules, and exam history.
- **Smart Test Environment**: Built-in scientific calculator and real-time timer protection (resilient to page reloads).
- **Result & Feedback Viewer**: Instant score reports for objective tests and detailed evaluation reviews.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.8, Flask, Werkzeug, WTForms |
| **Computer Vision** | OpenCV (DNN & Haar Cascades), NLTK |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 4, Pixel UI, SweetAlert2 |
| **Database** | SQLite (embedded zero-config) / PyMySQL (optional production) |
| **Code Execution** | Sphere Engine API / Custom interpreters |

---

## 🚀 Quick Start Guide

### Option A: One-Click Startup (Recommended for Windows)

Simply double-click:
```bat
run.bat
```
This automatically sets up the environment, seeds the local database, and launches the application.

---

### Option B: Manual Setup

1. **Clone or Extract the Project**:
   ```bash
   cd MyProctor.ai-AI-BASED-SMART-ONLINE-EXAMINATION-PROCTORING-SYSYTEM-main
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Open in Browser**:
   - Web application: [http://localhost:5000/](http://localhost:5000/)

---

## 🔑 Demo Test Credentials

| Role | Email | Password |
|---|---|---|
| **Professor / Teacher** | `teacher@exam.com` | `password123` |
| **Student** | `student@exam.com` | `password123` |

---

## 📁 Project Structure

```text
MyProctor.ai/
├── app.py                     # Main Flask server application
├── camera.py                  # Real-time video capture & proctoring streamer
├── face_detector.py           # Face & person detection module
├── face_landmarks.py          # Facial landmarks & gaze estimation
├── flask_mysqldb.py           # Database abstraction (SQLite + MySQL fallback)
├── DB/
│   └── quizapp.db             # Local SQLite database (pre-seeded)
├── models/                    # Computer vision weights & cascade models
├── static/                    # CSS, JS, vendor libraries, icons, audio
├── templates/                 # Jinja2 HTML templates
│   ├── layout.html            # Main site layout & footer
│   ├── professor_dashboard.html # Teacher dashboard
│   ├── student_dashboard.html   # Student portal
│   ├── give_test.html         # Test portal with camera checks
│   └── ...                    # Exam and admin templates
├── requirements.txt           # Python dependency list
├── run.bat                    # One-click startup script
└── README.md                  # Project documentation
```

---

## 👨‍💻 Developed By

**Yashvant**
- 🌐 **Portfolio**: [https://portfolio-jade-one-1cqukhqrqd.vercel.app/](https://portfolio-jade-one-1cqukhqrqd.vercel.app/)

---

<p align="center">
  Made with 💗 By <a href="https://portfolio-jade-one-1cqukhqrqd.vercel.app/">Yashvant</a>
</p>
