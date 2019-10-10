import os
from flask import Flask, render_template, request     
from flask import send_from_directory
from flask_bootstrap import Bootstrap
from glob import glob
import shutil
from azure.storage.blob import BlockBlobService, PublicAccess 

block_blob_service = BlockBlobService(account_name='dss', account_key='7DUevnSaIEacLBQ8M6Z6C9qAA1fMLWdRrh22zYUksqE+nxGoPiAd+6RZOaAGUiiAXe+YH6Kv13Yhuzm9sgI6zg==')
foldernames = block_blob_service.list_containers()
names = []
for events in foldernames:
    names.append(events.name)

#flask
app = Flask(__name__)
Bootstrap(app)

#home
@app.route("/")
def home():
    return render_template("index.html")

#get images from database
@app.route("/database/alert001/<filename>")
def get_images(filename):
    return send_from_directory("database/alert001",  filename)

#login page
@app.route("/login")
def login():
    return render_template("login.html", names = names)

#dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", names = names)

#request photos
@app.route("/photos", methods=['GET', 'POST'])
def get_photos():
    if len(os.listdir("./database"))>0:
        shutil.rmtree("./database/alert001")
    link = request.args.get('link', default='', type=str)
    print(link)
    generator_link = block_blob_service.list_blobs(link)
    os.mkdir("./database/alert001")
    for x in generator_link:
        block_blob_service.get_blob_to_path(link, x.name, "./database/alert001" + "/" + x.name)
    images = []
    for file in os.listdir("./database/alert001"):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            images.append(file)
    f=open("./database/alert001/timestamp.txt", "r")
    date =f.read()
    return render_template("photos.html", images = images, date=date)

#delete 
@app.route("/delete")
def del_photos():
    os.remove("/database/alert001")

    
if __name__ == "__main__":
    app.run()