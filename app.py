# استيراد المكتبات
from flask import Flask, render_template_string, request, jsonify
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64

# إعداد تطبيق Flask
app = Flask(__name__)

# تحميل نموذج Stable Diffusion
try:
    print("Loading Stable Diffusion model... (This may take a few minutes)")
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to("cuda")
except Exception as e:
    print(f"Error loading model: {e}")
    pipe = None

# واجهة الصفحة الرئيسية
html_template = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Image Generator</title>
    <style>
        /* تم الحفاظ على نفس التنسيقات */
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Image Generator</h1>
        {% if not model_loaded %}
            <p class="error">The model failed to load. Please check the server logs.</p>
        {% else %}
            <form id="generate-form" action="/generate" method="post">
                <!-- باقي الكود كما هو -->
            </form>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    model_loaded = pipe is not None
    return render_template_string(html_template, model_loaded=model_loaded)

@app.route('/generate', methods=['POST'])
def generate_image():
    if not pipe:
        return jsonify({"error": "Model not loaded"}), 500

    # نفس الكود كما هو لإدارة المدخلات
    try:
        # هذا هو مكان التعديل الذي طلبته
        print("This is inside the try block")
        # هنا يأتي باقي الكود الخاص بتوليد الصورة
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
