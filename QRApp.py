from flask import Flask
from flask import render_template
from flask import  request,redirect,url_for
import cv2
import time
from pyzbar import pyzbar
import qrcode
import os
import urllib.request
import urllib.parse
import json

from PIL import  Image

app=Flask(__name__)
@app.route('/')
def Home():
    print("Hello Welcome to QR App")
    return render_template('QRapp.html')
@app.route('/genAdd')
def genAdd():
    print('Entering the GenAddress Method')
    file=open('properties.json')
    data=json.load(file)
    #with open("properties.json", mode='r') as file:
     #        text=file.read()
    print(data['url']+" : url")
    url=data['url']
    req = urllib.request.urlopen(url)
    address=urllib.parse.parse_qs(urllib.parse.urlparse(req.url).query)['address'][0]
    return render_template('QRapp.html',data=address)

@app.route('/genQR',methods=['POST'])
def genQR():
    if request.method=='POST':
        print("QR generating....")
        address = request.form.get('address')
        print(address)
        img = qrcode.make(address)
        img.save("./static/"+address+".png")
    return render_template('genQR.html',data=address)
@app.route('/scanQR',methods=['POST'])
def scanQR():
    if request.method=='POST':
        print("scanning QR....")
        camera = cv2.VideoCapture(0)
        time.sleep(1.000)
        ret, frame = camera.read()
        while ret:
            ret, frame = camera.read()
            data = read_qrcodes(frame)
            cv2.imshow('QR code reader/ Press Esc to exit', data["frame"])
            if cv2.waitKey(1) & 0xFF == 27:
                break
        camera.release()
        cv2.destroyAllWindows()
        return render_template('QRapp.html',data=data["Text"])


def read_qrcodes(frame):
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        x, y, w, h = qrcode.rect
        # 1
        qrcode_info = qrcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, qrcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        # 3
        with open("code_result.txt", mode='w') as file:
            file.write(qrcode_info)
    with open("code_result.txt", mode='r') as file:
             text=file.read()
    return {"frame":frame,"Text":text}
if __name__=='__main__':
    app.run(debug=True)