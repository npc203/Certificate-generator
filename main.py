from flask import Flask, render_template, request,send_file
from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/single', methods=['POST'])
def single():
    name=request.form['name']
    return serve_img(generate(name))

@app.route('/list_upload', methods=['POST'])
def list_use():
    folder=str(int(time.time()))
    path='tmp/'+folder
    os.mkdir(path) 
    with request.files['file'] as f:
        for i in f.readlines():
            generate(i).save(path+f'/{i}.jpg')


def serve_img(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')  

def generate(message):
    image = Image.open('static/certificate.png')
    
    draw = ImageDraw.Draw(image)
    
    font = ImageFont.truetype('static/Ubuntu-Regular.ttf', size=20)

    (x,y) = (500,260)

    color = 'rgb(0,0,0)'

    draw.text((x,y), message, fill=color, font=font)

    (x1,y1) = (550,480)

    #save = message+'.png'

    draw.text((x1,y1), 'xyz', fill=color, font=font)

    #image.save('generated_certificates/'+save)

    return image



if __name__ == "__main__":
    app.run(debug=True)

