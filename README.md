# LearnSphere - Student Learning Portal

## Project Overview

LearnSphere is a web-based student learning portal developed using Django. It is designed to provide students with a centralized platform to access study materials, manage tasks, interact with peers, and utilize various educational tools.

The platform integrates multiple academic utilities into a single system, improving productivity and enhancing the learning experience.

---

## Features

* User registration and authentication system
* Notes management system (view and organize notes)
* Homework tracking system
* To-do task management
* YouTube integration for educational content
* Wikipedia search integration
* PDF to Audio conversion feature
* Unit and language conversion tools
* Group chat system for discussion
* Profile management
* Responsive dashboard interface

---

## Modules

### 1. Notes Module

* Create and view notes
* Organized academic content

### 2. Homework Module

* Track assignments
* Manage deadlines

### 3. To-Do Module

* Add and manage daily tasks

### 4. YouTube Integration

* Search and access educational videos

### 5. Wikipedia Integration

* Fetch and display information from Wikipedia

### 6. Conversion Module

* Unit conversion
* Language translation
* Mathematical conversions

### 7. PDF to Audio Converter

* Upload PDF files
* Convert text into audio format

### 8. Group Chat

* Real-time discussion between students and teachers

---

## Technologies Used

* Backend: Django (Python)
* Frontend: HTML, CSS, Bootstrap, JavaScript
* Database: SQLite (default Django database)
* Static Handling: WhiteNoise
* Additional Tools:

  * PDF processing libraries
  * Audio generation libraries

---

## Project Structure

```id="l9s2kd"
LearnSphere/
│
├── dashboard/
│   ├── templates/dashboard/
│   │   ├── home.html
│   │   ├── notes.html
│   │   ├── homework.html
│   │   ├── todo.html
│   │   ├── youtube.html
│   │   ├── wiki.html
│   │   ├── conversion.html
│   │   ├── audioplay.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   ├── login.html
│   │   └── groupchat.html
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── LearnSphere/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
├── manage.py
├── requirements.txt
├── runtime.txt
└── Procfile
```

---

## Installation and Setup

1. Clone the repository:

```id="b4q8mt"
git clone https://github.com/Shruti-Adam/LearnSphere.git
```

2. Navigate to project directory:

```id="t2w9lp"
cd LearnSphere
```

3. Create virtual environment:

```id="4j8kzm"
python -m venv venv
```

4. Activate virtual environment:

Windows:

```id="d1x7qh"
venv\Scripts\activate
```

5. Install dependencies:

```id="p9v3ya"
pip install -r requirements.txt
```

6. Run migrations:

```id="k2z7nr"
python manage.py migrate
```

7. Run server:

```id="s6m1xt"
python manage.py runserver
```

8. Open in browser:

```id="y3c9fd"
http://127.0.0.1:8000/
```

---

## Usage

* Register a new user account
* Login to access dashboard
* Use modules like Notes, Homework, and To-Do
* Search educational content via YouTube and Wikipedia
* Convert PDFs into audio
* Participate in group discussions

---

---

## Project Screenshots

<img width="1889" height="873" alt="image" src="https://github.com/user-attachments/assets/0a0095b0-d3d6-4527-82bc-07cd4adcbe88" />
<img width="1900" height="594" alt="image" src="https://github.com/user-attachments/assets/32b14399-9e6b-4c90-be76-f927354f53d1" />
<img width="1888" height="833" alt="image" src="https://github.com/user-attachments/assets/644dbf46-086d-4f86-809a-80e6530a1b23" />
<img width="1903" height="786" alt="image" src="https://github.com/user-attachments/assets/882ed5b9-161a-42bb-aee4-91fedde7a1e7" />
<img width="1875" height="881" alt="image" src="https://github.com/user-attachments/assets/e50478d2-4b2e-49a4-a6d0-08fd43d8d42e" />
<img width="1897" height="789" alt="image" src="https://github.com/user-attachments/assets/d24de8ae-8f71-470e-b166-154550738631" />
<img width="1907" height="866" alt="image" src="https://github.com/user-attachments/assets/83ffcca2-2bb3-414f-a8a0-20d6a43c63f0" />
<img width="1894" height="842" alt="image" src="https://github.com/user-attachments/assets/b2414b42-ad7e-4da3-af68-839da37fffb5" />
<img width="1889" height="831" alt="image" src="https://github.com/user-attachments/assets/78ce9b0c-8cb9-41ca-81d4-7059a109df10" />



---


## Developer

Shruti Adam
GitHub: https://github.com/Shruti-Adam

---

## Notes

LearnSphere is designed as a comprehensive academic platform that integrates multiple learning tools into a single system, making it useful for students to manage their academic activities efficiently.
