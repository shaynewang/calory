import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from lib import nutritionix as nx
from lib import vision as vs
from lib.translator import Translator

HOST = "0.0.0.0"
PORT = 8003
IMG_EXTN = set(["jpg","jpeg","png","tiff","bmp","gif"])

# remove for production
DOWNLOADS = "downloads" 
if not os.path.isdir(DOWNLOADS):
    os.mkdir(DOWNLOADS)

app = Flask(__name__)
nxapi = nx.api()
trans = Translator()

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
    food_info = set()

    # get list of labels using image path
    # expects image is in downloads/
    foods = vs.detect_image(os.path.abspath(os.path.join(DOWNLOADS, image)))
    for food in set(foods):
        print(food)
        food_info.add(nxapi.get_calories(food))
    languages = trans.available_languages()
    return render_template("info.html", food_info=food_info, food_info_en=food_info, languages=languages)

@app.route("/info/translated", methods=["POST"])
def translated():
    """
    Display translated information for foods
    """
    if request.method == "POST":
        food_info = []
        info = request.form["info"].split("\r\n")
        lang = request.form["lang"]
        food_info_en = [i for i in info if i.strip()]
        food_info = [trans.translate(i,lang) for i in info if i.strip()]
        languages = trans.available_languages()
    return render_template("info.html", food_info=food_info, food_info_en=food_info_en, languages=languages)


if __name__ == "__main__":
    app.run(host=HOST,port=PORT,debug=True)
