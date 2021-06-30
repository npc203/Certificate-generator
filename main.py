from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os,sys
import json
import zipfile
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./static/"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        if file1:  
            path = os.path.join(app.config['UPLOAD_FOLDER'], "certificate.png")
            file1.save(path)
        data = {"data":[]}
        with open( os.path.join(app.config['UPLOAD_FOLDER'], "info.json"),"w+") as f:
            for i,j in request.form.items():
                if i.endswith("_go"):
                    tmp = j.split("|")
                    data["data"].append({"msg":tmp[0],"x":tmp[1],"y":tmp[2]})
            f.write(json.dumps(data,indent=4))
        return serve_img(generate())
    return render_template("modal.html")

@app.route('/list', methods=['GET','POST'])
def list_use():
    if request.method == 'POST':
        # Making tmp cache dir
        folder=str(int(time.time()))
        path='tmp/'+folder
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')
        os.mkdir(path) 

        # Setting up data
        with open("static/info.json","r") as f:
            data = json.load(f)
        f=request.files['file']
        content = f.read().decode("ascii").replace('\r','').split('\n')
        zipf = zipfile.ZipFile('tmp/final.zip', 'w', zipfile.ZIP_DEFLATED)

        # stuff
        for raw_data in content:
                parse  = raw_data.split(",")
                fname=''.join(ch for ch in parse[0] if ch.isalnum())
                for i in range(len(data["data"])):
                    data["data"][i]["msg"] = parse[i]

                generate(data).save(path+f'/{fname}.jpg')
                zipf.write(os.path.join(path,f'{fname}.jpg'),arcname=f'{fname}.jpg')
        zipf.close()

        return send_file('tmp/final.zip', attachment_filename='Certificates.zip',as_attachment=True)
    return render_template("list.html")


def serve_img(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, "JPEG", quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")

def generate(data=None):
    image = Image.open("static/certificate.png")
    if not data:
        with open("static/info.json","r") as f:
            data = json.load(f)

    #Aspect resize
    basewidth = 800
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)

    #Drawing things
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/poppins.ttf", size=20)
    color = "rgb(0,0,0)"
    for item in data["data"]:
        draw.text((int(item['x']),int(item['y'])), item["msg"], fill=color, font=font)

    image = image.convert('RGB')
    return image


if __name__ == "__main__":
    app.run(debug=True)
