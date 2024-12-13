# استخدم صورة Python الرسمية
FROM python:3.10-slim

# تثبيت المتطلبات
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الملفات وتشغيل التطبيق
COPY . .
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
