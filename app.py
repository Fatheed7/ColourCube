from flask import Flask, send_file, request, render_template
from PIL import Image
from io import BytesIO
import os

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/<int:h>/<int:w>/<int:r>/<int:g>/<int:b>')
@app.route('/<int:h>/<int:w>/<int:r>/<int:g>/<int:b>/')
def generate_image(h, w, r, g, b):

    error_message = check_values(h, w)
    if error_message:
        return error_message

    image = Image.new('RGB', (w, h), color=(r, g, b))

    image_stream = BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')

def check_values(h, w):
    switch = {
        h > 150: "Please enter a height below 100 pixels",
        w > 150: "Please enter a width below 100 pixels"
    }
    return switch.get(True, None)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
