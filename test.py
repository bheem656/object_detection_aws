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
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov5s"

# send = { }
# def result_append(res):
#     send = res.append(send)

# def final():
#         ret = eval(send)
#         ret = json.dumps(ret)
#         return ret

result_1 = {}


def process(image_file):
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        height = img.height
        results = model(img)
        temp = results.pandas().xyxy[0].to_json(orient="records")
        res = convert(temp,height)
        # result_append(res)
        # result = eval(res)
        # result = json.dumps(res)

        return (res)

@app.route('/upload')
def home_upload():
    return render_template('u_f.html')

@app.route('/upload', methods=['POST'])
def garuda_solar_train_folder():
    if os.path.exists("temp4.json"):
        os.remove("temp4.json")
    else:
        print("The file does not exist")
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        # f = request.files['file']

        for file in files:
            f1 = secure_filename(file.filename)
            # print(f1)

            # image_file = request.files[file]
            z = process(file)
            # print(z)
            # print("process")
            # print(type(temp1))
            x1 = {"img_name": f1,
                "id": 1    
                }
            x1["data"] = z
            result_1["img1"]=x1
            
            with open('temp4.json', 'a') as f:
                 json.dump(result_1, f)
                #  json.dump(",", f)
                 f.close()  

        with open('temp4.json', 'r') as f1:
        #    json.dump(result_1, f)                  
            rrs = f1.read()
            # xx = f.read()
            # rr = json.loads(xx)
            print(rrs)
            # rr = json.loads(rrs)
            return (rrs)
            # z = json.loads(res)
        #     # res = res.append(z)
        # sends = final()
        # return sends
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # flash('File(s) successfully uploaded')

@app.route(DETECTION_URL)
def home():
    return render_template('detection.html')

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        height = img.height
        results = model(img)
        temp = results.pandas().xyxy[0].to_json(orient="records")
        res = convert(temp,height)
        # result = eval(res)
        result = json.dumps(res)
        return (result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    app.run(host="0.0.0.0", port=args.port, debug=True)  # debug=True causes Restarting with stat
