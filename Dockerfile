FROM python:3.10-slim

# تثبيت المتطلبات الأساسية للنظام
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# إعداد العمل
WORKDIR /app

# نسخ متطلبات Python وتثبيتها
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# تعيين متغير بيئي لتحديد التطبيق
ENV FLASK_APP=app.py

# تشغيل التطبيق باستخدام gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
