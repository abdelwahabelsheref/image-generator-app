FROM python:3.9-slim

# إعداد البيئة
WORKDIR /app

# تثبيت حزم النظام المطلوبة (بما في ذلك distutils)
RUN apt-get update && apt-get install -y \
    python3-distutils \
    python3-apt \
    && apt-get clean

# نسخ متطلبات المشروع
COPY requirements.txt .

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تعريف المنفذ
EXPOSE 5000

# تشغيل التطبيق
CMD ["python", "app.py"]
