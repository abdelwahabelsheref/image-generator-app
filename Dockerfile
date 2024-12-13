FROM python:3.9-slim

# تثبيت المتطلبات
RUN apt-get update && apt-get install -y git wget && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الملفات
COPY . /app
WORKDIR /app

# كشف المنفذ
EXPOSE 8000

# تشغيل التطبيق
CMD ["python", "app.py"]
