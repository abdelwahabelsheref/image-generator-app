# استيراد المكتبات
from flask import Flask, render_template_string, request, jsonify
from diffusers import StableDiffusionPipeline
import torch
from pyngrok import ngrok
from PIL import Image
import io
import base64
import subprocess

# إعداد تطبيق Flask
app = Flask(__name__)

# تحميل نموذج Stable Diffusion
print("Loading Stable Diffusion model... (This may take a few minutes)")
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to("cuda")

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
            text-align: center;
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #4CAF50;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #4CAF50;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        img {
            max-width: 100%;
            margin-top: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .error {
            color: red;
            font-weight: bold;
        }
        .footer {
            margin-top: 20px;
            font-size: 14px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Image Generator</h1>
        <form id="generate-form" action="/generate" method="post">
            <input type="text" name="prompt" placeholder="Enter a prompt (e.g., a sunset over a mountain)" required>
            <br><br>
            <label for="format">Image Format:</label>
            <select name="format" id="format">
                <option value="png">PNG</option>
                <option value="jpeg">JPEG</option>
            </select>
            <br><br>
            <label for="quality">Quality (for JPEG only):</label>
            <select name="quality" id="quality">
                <option value="75">Medium</option>
                <option value="90">High</option>
                <option value="100">Very High</option>
            </select>
            <br><br>
            <button type="submit">Generate</button>
        </form>
        <div id="result">
            {% if error %}
                <p class="error">{{ error }}</p>
            {% elif image %}
                <h2>Generated Image:</h2>
                <img src="data:image/png;base64,{{ image }}" alt="Generated Image">
                <br>
                <a href="data:image/png;base64,{{ image }}" download="generated_image.png">Download Image</a>
            {% endif %}
        </div>
        <div class="footer">
            <p>Powered by Stable Diffusion</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    image_format = request.form['format']
    quality = int(request.form['quality']) if image_format == "jpeg" else None

    # تحسين البرومبتات (إضافة التفاصيل الواقعية)
    if prompt.lower() == "sunset over a mountain":
        prompt = "A breathtaking sunset over a snow-covered mountain, with the sky painted in shades of orange, pink, and purple, and the sun just above the horizon."
    elif prompt.lower() == "futuristic city":
        prompt = "A futuristic cityscape at night, with towering glass skyscrapers, neon signs flashing, flying cars zooming through the air, and a vibrant bustling street filled with people walking and robots working in the background."
    elif prompt.lower() == "lion in the wild":
        prompt = "A realistic close-up of a majestic lion with a thick golden mane, standing tall on a rocky cliff, with the sun casting dramatic shadows across its face, and the savannah stretching out in the background under a bright blue sky."
    elif prompt.lower() == "magical forest":
        prompt = "A magical forest with glowing trees, sparkling rivers, and mystical creatures flying around, under a starry sky filled with glowing constellations."
    elif prompt.lower() == "warrior princess":
        prompt = "A warrior princess with golden armor, holding a glowing sword, standing on a cliff at sunset, her long hair blowing in the wind, with a magical energy aura around her, and a distant kingdom in the background."
    elif prompt.lower() == "dragon in the sky":
        prompt = "A majestic dragon soaring through a dark stormy sky, with its wings spread wide, scales glistening in the flashes of lightning, and glowing eyes piercing through the dark clouds."
    elif prompt.lower() == "desert clock":
        prompt = "A surreal scene of a giant clock melting over a desert landscape, with the hands of the clock distorted and draped over the sand, under a bright blue sky with distant mountains in the background."

    try:
        print(f"Generating image for prompt: {prompt}")
        image = pipe(prompt, num_inference_steps=50).images[0]

        # تحويل الصورة إلى الصيغة المختارة (PNG أو JPEG)
        buffer = io.BytesIO()

        if image_format == "jpeg":
            image.save(buffer, format="JPEG", quality=quality)
        else:
            image.save(buffer, format="PNG")
        
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')

        return render_template_string(html_template, image=img_str)
    except Exception as e:
        print(f"Error generating image: {e}")
        return render_template_string(html_template, error="An error occurred while generating the image. Please try again.")

# تشغيل Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

# توصيل التطبيق بالإنترنت باستخدام ngrok
print("Starting ngrok...")
public_url = ngrok.connect(8000)
print(f"Your app is live at: {public_url}")
