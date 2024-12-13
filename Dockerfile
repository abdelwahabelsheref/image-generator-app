FROM python:3.9-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y git wget ffmpeg libgl1 && rm -rf /var/lib/apt/lists/*

# نسخ وإعداد المتطلبات
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الملفات
COPY . /app
WORKDIR /app

# كشف المنفذ
EXPOSE 8000

# تشغيل التطبيق
CMD ["python", "app.py"]
