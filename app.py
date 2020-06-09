from flask import Flask, request,render_template,redirect,jsonify,json
from werkzeug.utils import secure_filename
import base64
import hashlib
import time
import os
d={}
app = Flask(__name__)
@app.route("/") 
def index():
    return render_template("upload_image.html")
app.config["IMAGE_UPLOADS"]=r"C:\Users\win-10\flask\image"
app.config["ALLOWED_IMAGE_EXT"]=["JPEG","PNG","JPG"]
app.config["MAX_IMAGE_SIZE"]=0.5*1024*1024

def allowed_image(filename):
    

    if not"." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXT"]:
        
        return True
    else:
        return False
    
def allowed_size(filesize):
    if int(filesize)<=app.config["MAX_IMAGE_SIZE"]:
        return True
    else:
        return False

@app.route("/success",methods=['GET','POST'])


def success():
    d={}
    new=""
    if request.method=="POST":
        
        if request.files:

                image=request.files["image"]

                if image.filename=="":

                    print("No Filename")
                    return redirect(request.url)
                if allowed_image(image.filename):

                    filename=secure_filename(image.filename)


                    date_string = time.strftime("%Y-%m-%d-%H:%M") 
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"] + date_string +image.filename))

                    add=os.path.join(app.config["IMAGE_UPLOADS"] + date_string +image.filename)
                    #print(add)
                    image1=open(add,'rb')
                    image_read=image1.read()
                    image_64_encode=base64.encodestring(image_read)
                    hashcode=hashlib.md5(image_64_encode)
                    new=image_64_encode.decode('utf-8')
                    d={'h':new}
        print(type(d))
        return json.dumps(d)
    else:
        return redirect(request.url) 
if __name__ == "__main__":
    app.run()
