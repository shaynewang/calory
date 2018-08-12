import os
import threading
from flask import Flask, render_template, request, redirect, url_for
from flask_sslify import SSLify
from werkzeug.utils import secure_filename

from lib import foodinfo as finfo
from lib import vision as vs
from lib.translator import Translator

HOST = "0.0.0.0"
PORT = 8080
IMG_EXTN = set(["jpg","jpeg","png","tiff","bmp","gif"])

FORCE_HTTPS = False
# remove for production
DOWNLOADS = "static/downloads" 
if not os.path.isdir(DOWNLOADS):
    os.mkdir(DOWNLOADS)

app = Flask(__name__)
if FORCE_HTTPS: sslify = SSLify(app,subdomains=True)
trans = Translator()

def is_image_file(filename):
    """
    Returns True if filename has an image extension
    Otherwise return False
    """
    return "." in filename and filename.split(".")[-1].lower() in IMG_EXTN

def get_calories_threaded(food,food_info):
    food_info.add(finfo.get_calories(food))

def translate_threaded(i,lang,food_info):
    food_info.add(trans.translate(i,lang))

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
    return render_template("upload.html")

@app.route("/info/<image>")
def info(image):
    """
    Display information for foods
    """
    food_info = set()

    # get list of labels using image path
    # expects image is in downloads/
    image_path = os.path.join(DOWNLOADS,image)
    try:
        foods = vs.detect_image(image_path)
        # remove image file after food labels are detected
        #os.remove(image_path)
    except:
        return redirect(url_for("upload"))
    queue = []

    # assign jobs to minions(Bob, Kevin, etc...)
    for food in set(foods):
        minion = threading.Thread(target=get_calories_threaded, args=(food,food_info,))
        queue.append(minion)
        minion.start()

    # collect results from the minions
    for minion in queue:
        minion.join()

    if '' in food_info: food_info.remove('')
    if not food_info or food_info == (''):
        food_info.add("No calories information found...")
    languages = trans.available_languages()
    return render_template("info.html",image=image, food_info=food_info, food_info_en=food_info, languages=languages)

@app.route("/info/translated", methods=["POST"])
def translated():
    """
    Display translated information for foods
    """
    if request.method == "POST":
        food_info = set()
        info = request.form["info"].split("\r\n")
        lang = request.form["lang"]
        image = request.form["image"]
        food_info_en = [i for i in info if i.strip()]
        queue = []
        for i in food_info_en:
            minion = threading.Thread(target=translate_threaded, args=(i,lang,food_info,))
            queue.append(minion)
            minion.start()

        for minion in queue:
            minion.join()

        languages = trans.available_languages()
    return render_template("info.html",image=image, food_info=food_info, food_info_en=food_info_en, languages=languages)


if __name__ == "__main__":
    app.run(host=HOST,port=PORT,debug=not FORCE_HTTPS)
