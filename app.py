from flask import Flask, send_file, request, render_template, redirect, url_for
from PIL import Image
from io import BytesIO
import os

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

#Home Route
@app.route("/")
def home():
    #Return index.html if this route is called.
    return render_template("index.html")

#ColourCube Route
#This Route expects various integer values to be provided.
#For example: /25/50/200/150/100/
#If this format is not followed, the invalid_route 
#route is called.
@app.route('/<int:h>/<int:w>/<int:r>/<int:g>/<int:b>')
@app.route('/<int:h>/<int:w>/<int:r>/<int:g>/<int:b>/')
def generate_image(h, w, r, g, b):

    #Call check_values function, and pass it the
    #height, width, red, green and blue values.
    error_message = check_values(h, w, r, g, b)
    #If error_message is true
    if error_message:
        #Return the error template and pass the error message
        return render_template("error.html", error=error_message)

    #Create a new image using Pillow, setting the
    #height, width, red, green and blue values
    image = Image.new('RGB', (w, h), color=(r, g, b))

    #BytesIO creates an in-memory stream
    image_stream = BytesIO()
    #Save the image to the BytesIO stream
    image.save(image_stream, format='PNG')
    #Read the data from the image_stream variable
    #seek(0) ensures we start at the beginning 
    #of the data
    image_stream.seek(0)

    #Return the image to the browser as a PNG
    return send_file(image_stream, mimetype='image/png')


def check_values(h, w, r, g, b):
    #Dictionary created containing error messages
    #Each condition is checked and if true, the
    #relevant error message is returned
    switch = {
        #Check if Height is greater than 150
        h > 150: "Please enter a height below 150 pixels",
        #Check if Width is greater than 150
        w > 150: "Please enter a width below 150 pixels",
        #Check if Red, Green and Blue are integers.
        not isinstance(r, int) or not isinstance(g, int) or not isinstance(
            b, int): (
                "Please enter valid integers for the "
                "red, green, and blue values."),
        #Check if Red, Green and Blue are between 0 and 255
        not (0 <= r <= 255) or not (0 <= g <= 255) or not (
            0 <= b <= 255): ("Please enter red, green, and blue "
                             "values between 0 and 255.")
    }
    #Check the conditions in the switch dictionary.
    #If any values are true, return true. Otherwise,
    #return None
    return switch.get(True, None)

#Route to capture any invalid URLs entered.
#This route will be called instead of a standard
#error message.
@app.route('/<path:invalid_route>')
def invalid_route(invalid_route):
    #Return 404.html if this route is called
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
