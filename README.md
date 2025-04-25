# 🚀 Multi-Container Flask App with Redis

This project demonstrates a simple **Flask web application** that counts the number of times a user has visited the site. It uses **Redis** for storing the counter and **Docker Compose** for managing multi-container orchestration.

---

## 📁 Project Structure

```
multi-container-app/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container setup for Flask app
├── docker-compose.yml     # Multi-container orchestration
└── templates/
    └── index.html         # Jinja2 template for rendering the web page
```

---

## 🛠️ Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## ⚙️ Step-by-Step Setup Guide

### 1. ✅ Clone the Repository

```bash
git clone https://github.com/your-username/multi-container-app.git
cd multi-container-app
```

---

### 2. 🐍 Create `requirements.txt`

```txt
Flask
redis
```

---

### 3. 🧱 Build Your Flask App (`app.py`)

```python
from flask import Flask, render_template
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    try:
        return cache.incr('hits')
    except redis.exceptions.ConnectionError:
        return 'Redis connection error.'

@app.route('/')
def index():
    count = get_hit_count()
    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

---

### 4. 🖼 Create `index.html` Template

Make sure the file is UTF-8 encoded!

**File:** `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask with Redis</title>
</head>
<body>
    <h1>Hello! You've visited this page {{ count }} times.</h1>
</body>
</html>
```

---

### 5. 🐳 Dockerfile (Flask App Image)

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

---

### 6. ⚙️ `docker-compose.yml` (Orchestration)

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    depends_on:
      - redis

  redis:
    image: "redis:alpine"
```

---

### 7. 🚀 Build and Run Containers

```bash
docker-compose up --build
```

Visit **http://localhost:5000** to see your app in action!

---

## ❗ Common Errors and Fixes

### 🔴 Error: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff...`

**Cause:** The `index.html` file is not UTF-8 encoded.

**Fix:**
- Open the file in VS Code or Notepad++
- Re-save the file with UTF-8 encoding:
  - In VS Code: `Reopen with Encoding → UTF-8`, then `Save with Encoding → UTF-8`
  - In Notepad++: `Encoding → Convert to UTF-8`

Then restart your containers:

```bash
docker-compose down
docker-compose up --build
```

---

## ✅ Best Practices

- Ensure all template files are UTF-8 encoded.
- Use `depends_on` to ensure service startup order.
- Use `volumes` in development for live reload (optional with Flask debug mode).
- Don't use debug mode in production containers.

---

## 📜 License

This project is licensed under the MIT License.

