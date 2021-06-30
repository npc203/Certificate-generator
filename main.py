from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os,sys
import json
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./static/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/single", methods=["POST"])
def single():
    name = request.form["name"]
    return serve_img(generate(name))


def serve_img(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, "JPEG", quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")

@app.route('/new', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        if file1:  
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            file1.save(path)
        data = {"data":[]}
        with open( os.path.join(app.config['UPLOAD_FOLDER'], "info.json"),"w+") as f:
            for i,j in request.form.items():
                if i.endswith("_go"):
                    tmp = j.split("|")
                    data["data"].append({"msg":tmp[0],"x":tmp[1],"y":tmp[2]})
            f.write(json.dumps(data,indent=4))

        return f"{request}<br><br>{request.form}<br><br>{request.data})"
    
    return render_template("modal.html")

def generate(message):
    image = Image.open("static/certificate.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/Ubuntu-Regular.ttf", size=20)
    color = "rgb(0,0,0)"
    with open("static/info.json","r") as f:
        data = json.load(f)
    item = data["data"].pop(0)
    draw.text((int(item['x']),int(item['y'])), message, fill=color, font=font)
    for item in data["data"]:
        draw.text((int(item['x']),int(item['y'])), item["msg"], fill=color, font=font)
    return image


if __name__ == "__main__":
    app.run(debug=True)
