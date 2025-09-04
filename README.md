# IP Tracking & Anomaly Detection

This project is a Django application designed to log and analyze incoming web requests to identify and flag suspicious IP addresses. It combines real-time request logging with advanced rate limiting and a background machine learning task for anomaly detection.

## Features

- Real-time Request Logging: All incoming requests are logged to the database, capturing the IP address, timestamp, URL path, and geolocation data. This provides a rich dataset for analysis.
- IP Geolocation: The django-ipgeolocation library is used to automatically enrich each request log with country and city information, providing valuable context for analysis.
- Smart Rate Limiting: The application uses django-ratelimit to protect sensitive endpoints from brute-force attacks. The /login/ endpoint is configured with the following limits:
  - Anonymous Users: 5 requests per minute, limited by IP address.
  - Authenticated Users: 10 requests per minute, limited by user ID.
- Advanced Anomaly Detection: A powerful Celery task runs hourly to identify suspicious behavior. It combines two core methods:
  - Rule-Based Flagging: Automatically flags any IP address that exceeds 100 requests per hour or attempts to access sensitive paths like /admin/ or /login/.
  - Machine Learning Model: Uses a scikit-learn Isolation Forest model to detect IPs that are statistical outliers based on request volume and path uniqueness. This helps identify complex, bot-like behavior that simple rules might miss.

## Installation & Setup

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later
- Django 3.2 or later
- PostgreSQL 12 or later
- Docker & Docker Compose (for running Redis)

1. Clone the repository:

```bash
git clone https://github.com/olaishola05/alx-backend-security.git
cd alx-backend-security
```

2. Install Python dependencies:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt
```

Note: A requirements.txt file can be generated with pip freeze > requirements.txt after installing all the necessary packages.

3. Run Redis with Docker
This project relies on Redis for Celery and caching. You can start it using Docker Compose.

```bash
# Start Redis
docker-compose up -d redis
```

4. Run Migrations and Start the Django Server

Set up the database and run the Django development server.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

5. Start Celery Worker and Beat

The anomaly detection task requires both a Celery worker and the Celery Beat scheduler. Run each in a separate terminal window.

```bash
# Start Celery worker
celery -A your_project_name worker --loglevel=info

# Start Celery Beat
celery -A your_project_name beat --loglevel=info
```

5. Start Celery Worker and Beat

The anomaly detection task requires both a Celery worker and the Celery Beat scheduler. Run each in a separate terminal window.

```bash
# Terminal 1: Start the Celery worker
celery -A your_project_name worker --loglevel=info

# Terminal 2: Start the Celery Beat scheduler
celery -A your_project_name beat --loglevel=info
```

Usage

- Triggering Rate Limits: Access the /login/ endpoint in your browser. You will be limited to 5 requests per minute.

- Viewing Logs & Suspicious IPs: After running the application, you can view the RequestLog and SuspiciousIP tables in the Django Admin panel at <http://127.0.0.1:8000/admin/>. The flag_suspicious_ips task will populate the SuspiciousIP model every hour.
