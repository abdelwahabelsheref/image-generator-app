from flask import Flask, render_template_string, request, jsonify
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64

# إعداد تطبيق Flask
app = Flask(__name__)

# تحميل نموذج Stable Diffusion على CPU (بدلاً من GPU)
try:
    print("Loading Stable Diffusion model... (This may take a few minutes)")
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32).to("cpu")  # استخدام CPU بدلاً من GPU
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
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }
        .container {
            width: 80%;
            margin: 50px auto;
            text-align: center;
        }
        .container h1 {
            color: #333;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 10px;
            width: 80%;
            max-width: 600px;
            margin-bottom: 20px;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .image-container {
            margin-top: 30px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Image Generator</h1>
        {% if not model_loaded %}
            <p class="error">The model failed to load. Please check the server logs.</p>
        {% else %}
            <form id="generate-form" action="/generate" method="post">
                <input type="text" name="prompt" placeholder="Enter prompt for image generation" required>
                <button type="submit">Generate Image</button>
            </form>
            {% if image %}
                <div class="image-container">
                    <h3>Generated Image:</h3>
                    <img src="data:image/png;base64,{{ image }}" alt="Generated Image">
                </div>
            {% endif %}
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

    # قراءة المدخلات من النموذج
    prompt = request.form.get('prompt', '')  # الحصول على النص المطلوب لتوليد الصورة
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        print("Generating image for prompt:", prompt)
        image = pipe(prompt).images[0]  # توليد الصورة بناءً على النص المدخل
        # تحويل الصورة إلى base64 لعرضها في المتصفح
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return render_template_string(html_template, model_loaded=True, image=img_str)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
