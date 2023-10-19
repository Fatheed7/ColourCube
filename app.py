from flask import Flask, send_file, request, render_template, redirect, url_for
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

    error_message = check_values(h, w, r, g, b)
    if error_message:
        return render_template("error.html", error=error_message)

    image = Image.new('RGB', (w, h), color=(r, g, b))

    image_stream = BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')


def check_values(h, w, r, g, b):
    switch = {
        h > 150: "Please enter a height below 100 pixels",
        w > 150: "Please enter a width below 100 pixels",
        not isinstance(r, int) or not isinstance(g, int) or not isinstance(
            b, int): (
                "Please enter valid integers for the"
                "red, green, and blue values."),
        not (0 <= r <= 255) or not (0 <= g <= 255) or not (
            0 <= b <= 255): ("Please enter red, green, and blue"
                             "values between 0 and 255.")
    }
    return switch.get(True, None)


@app.route('/<path:invalid_route>')
def invalid_route(invalid_route):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
