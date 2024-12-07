from flask import Flask, render_template, request
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import base64
import io
import threading

app = Flask(__name__)

# تحميل النموذج
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to("cuda")


@app.route('/')
def home():
    return '''
    <!doctype html>
    <title>AI Image Generator</title>
    <h1>Enter a Prompt to Generate an Image</h1>
    <form action="/generate" method="post">
        <input type="text" name="prompt" placeholder="Enter a prompt" required>
        <button type="submit">Generate</button>
    </form>
    '''


@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    image = pipe(prompt, num_inference_steps=30).images[0]

    # تحويل الصورة إلى بيانات Base64 لعرضها في المتصفح
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')

    # واجهة لعرض الصورة الناتجة
    return f'''
    <!doctype html>
    <title>Generated Image</title>
    <h1>Generated Image for: "{prompt}"</h1>
    <img src="data:image/png;base64,{img_str}" alt="Generated Image">
    <br><br>
    <a href="/">Generate Another Image</a>
    '''


# تشغيل التطبيق
def run_app():
    app.run(host='0.0.0.0', port=5000)


thread = threading.Thread(target=run_app)
thread.start()
