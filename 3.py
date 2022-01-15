"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import json
import torch
from flask import Flask, request, render_template
from PIL import Image
from change_origin import convert
# from werkzeug.utils import secure_filename
import os
import requests
from flask_cors import CORS, cross_origin
# from io import BytesIO
from flask import jsonify, make_response


app = Flask(__name__)


CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# CORS(app, support_credentials=True)
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

DETECTION_URL = "/v1/transmission_line/yolov5s"

temp = {
    "Detected_payload": [
        {
            "images": [
                {
                    "Gufi": "8bf2d25b-fe18-4b09-b6bb-6735c5324aab",
                    "MediaFileId": 42479,
                    "MemberIds": 236,
                    "MissionId": 570,
                    "path": "https://imgd.aeplcdn.com/0x0/n/cw/ec/56265/f-pace-exterior-right-front-three-quarter-2.jpeg"
                },
                {
                    "Gufi": "8bf2d25b-fe18-4b09-b6bb-6735c5324aab",
                    "MediaFileId": 42463,
                    "MemberIds": 416,
                    "MissionId": 570,
                    "path": "https://media.istockphoto.com/photos/red-apple-picture-id184276818?k=20&m=184276818&s=612x612&w=0&h=QxOcueqAUVTdiJ7DVoCu-BkNCIuwliPEgtAQhgvBA_g="
                }
            ],
            "issueToBeDetected": [
                {
                    "AnnotationTypeId": 211,
                    "Name": "Broken"
                }
            ],
            "memberId": 236
        }
    ]
}


@app.route("/boticx", methods=["GET","POST"])
def helloWorld():
  # return "Hello, cross-origin-wor
  return (temp)

def process(image_file):
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        height = img.height
        results = model(img)
        temp = results.pandas().xyxy[0].to_json(orient="records")
        res = convert(temp,height)
        print(res)
        # result_append(res)
        # result = eval(res)
        # result = json.dumps(res)

        return (res)

def process_url(im):
        img = Image.open(im)
        height = img.height
        print("name:",img)
        print("name1:",im)
        results = model(img)
        print("model output", results.pandas().xyxy[0])
        temp = results.pandas().xyxy[0].to_json(orient="records")
        print("temp after result:",temp)
        res = convert(temp,height)
        # result_append(res)
        # result = eval(res)
        # result = json.dumps(res)
        #temp.clear()
        return (res)



# garuda_url = '/garuda_poc'
mylist = []
mydata = []
mysend = []


def extract_path(x1):
    print("inside extract, lenth ", len(x1))
    for p in range(0,(len(x1))):
        print("p:", p)
        for y in range(0,(len(x1[p]['images']))):
            print("y:",y)
            i1 = (x1[p]['images'][y]['path'])
            print("i1",i1)
            mylist.append(i1)
            # print(mylist)
    print("len " ,len(mylist))
    return mylist


@app.route(DETECTION_URL, methods=["GET", "POST"])
def starting_url():
    content_type = request.headers.get('Content-Type')
    # json.clear()
    mylist.clear()
    if (content_type == 'application/json'):
        json = request.json
        #print(json)
        mysend = json
        imag_data = extract_path(json)
        total = len(imag_data)
        print("len image ", total)
        #json.clear()
    else:
        return 'Content-Type not supported!'

    #for a in range(0,total,1):
    a = 0
    while a < total :
        print("a:", a)
        print("image_data", (len(imag_data)))
        response = requests.get(imag_data[a])
        image_bytes = io.BytesIO(response.content)
        converted_data = process_url(image_bytes)
        print("converted data:", converted_data)
        mysend[0]['images'][a]['data'] = converted_data
        a += 1
        # print(converted_data)

    payload = {'Detected_payload': mysend}
    # mysend.clear()
    print(payload)
    # payload.headers.add('Access-Control-Allow-Origin', '*')
    #m = json.dumps(mysend)

    # response = make_response(jsonify({"payload": mysend, "severity": "danger"}),401,)
    # response.headers["Content-Type"] = "application/json"
    #mylist.clear()
    #json.clear()
    return( payload)
    #print(type(payload))
    #t = json.loads(payload)
    #return (t)
    # return (payload)
    # return make_response(jsonify(payload), 200)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    # model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    model = torch.hub.load("ultralytics/yolov5", 'custom', path = 'best.pt')
    app.run(host="0.0.0.0", port=args.port, debug=True)  # debug=True causes Restarting with stat
