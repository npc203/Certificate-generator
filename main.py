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
    data={}
    f=request.files['file']
    names = f.read().decode("ascii").replace('\r','').split('\n')
    zipf = zipfile.ZipFile('tmp/final.zip', 'w', zipfile.ZIP_DEFLATED)
    for i in names:
        try:
            print('###############',i)
            generate(i).save(path+f'/{i}.jpg')
            zipf.write(os.path.join(path,f'{i}.jpg'),arcname=f'{i}.jpg')
            data[i]='Completed'
        except Exception as e:
            print('Warning:',e.__cause__)
            data[i]=str(e)
    zipf.close()
    return render_template('download.html',data=data)

@app.route('/download')
def download():
    return send_file('tmp/final.zip', attachment_filename='Certificates.zip',as_attachment=True)

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

