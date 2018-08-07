import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from lib import nutritionix as nx

HOST = "0.0.0.0"
PORT = 8003
IMG_EXTN = set(["jpg","jpeg","png","tiff","bmp","gif"])

# remove for production
DOWNLOADS = "downloads" 
if not os.path.isdir(DOWNLOADS):
    os.mkdir(DOWNLOADS)

app = Flask(__name__)
nxapi = nx.api()

def is_image_file(filename):
    """
    Returns True if filename has an image extension
    Otherwise return False
    """
    return "." in filename and filename.split(".")[-1].lower() in IMG_EXTN

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/submit", methods=["GET","POST"])
def submit():
    """
    View for file submission
    """
    if request.method == "POST":
        if "file" in request.files:
            image = request.files["file"]
            if image.filename != "" and is_image_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(DOWNLOADS,filename))
    return redirect("upload") # redirect here is handled by Dropzone

@app.route("/info/<image>")
def info(image):
    """
    Display information for foods
    """
    food_info = []
    # process image to get a list of food names
    if image == "test.jpg":
        foods = ["granny smith apple","pepperoni pizza","coke"]
    for food in foods:
        food_info.append(nxapi.get_calories(food))
    return render_template("info.html", food_info=food_info)

if __name__ == "__main__":
    app.run(host=HOST,port=PORT,debug=True)
