from flask import Flask, render_template, request, redirect, url_for
import json
# import ocrspace
import requests
# api = ocrspace.API()
import os
from ib import ib_image
from textExtract import textExtract
from textProcess import readFile, parseText, extractKeyValue, convertToJson
app = Flask(__name__)
filepath=""
orig_name=""
@app.route('/', methods=['GET', 'POST'])
def index():
    global orig_name
    filepath = "NOT FOUND"
    accuracy=0
    final=''
    Keymax=''
    if request.method == 'POST':
        file = request.files['images']
        print(file)
        orig_name=file.filename
    
        if not os.path.isdir('static'):
            os.mkdir('static')


        
        if not os.path.isdir('static/assets'):
            os.mkdir('static/assets')

        if os.path.isfile("static/assets/images.jpg"):
            os.remove("static/assets/images.jpg") 
        
        filepath = os.path.join('static/assets/', file.filename)
        newName = "static/assets/images.jpg"
        
        file.save(filepath)
        fp = os.rename(filepath, newName)
        
        
            
        return redirect(url_for('model'))


    return render_template('index.html', filepath=filepath)


@app.route('/model', methods=['GET', 'POST'])
def model():

    if request.method == 'POST':
        return redirect(url_for('im_process'))

    return render_template('model.html', filepath=filepath)

@app.route('/im_process', methods=['GET', 'POST'])
def im_process():
    ib_image(os.path.join('static/assets', 'images.jpg'))
    text=''

    filepath = os.path.join('static/augumentedImages', 'image.png')
    if request.method == 'POST':
        
        return redirect(url_for('result'))
    

    return render_template('ib.html', filepath=filepath, text=text)

@app.route('/result', methods=['GET', 'POST'])
def result():
    #open file and read the text
    textExtract(os.path.join('static/augumentedImages','image.png'))
    report=''
    text = readFile(os.path.join('static/healthRecords','recognized.txt'))
    #parse the text and extract the key value pairs
    keyValue = parseText(text)
    #convert the key value pairs to json
    text = extractKeyValue(sentences=keyValue)
    text = convertToJson(text)
    json_path = os.path.join('static/healthRecords','text.json')
    #Save the json
    with open(json_path, 'w') as outfile:
        json.dump(text, outfile)

    #Read the json
    with open(json_path, 'r') as f:
        text = json.load(f)

    croppedimages =[1, 2, 2]
    #Iterate over static\assets\croppedimages and get the names of the images

    for filename in os.listdir('static/assets/croppedimages'):
        croppedimages.append("static/assets/croppedimages/"+filename)
    
    for i in croppedimages:
        print(i)
    # Iterate over the json and get the names of the images
    

    # Return the json to the frontend

    if request.method == 'POST':
        return redirect(url_for('rectangle'))
    

    


    return render_template('json.html', text=text, croppedimages=croppedimages)


@app.route('/rectangle', methods=['GET', 'POST'])
def rectangle():
    return render_template('rect.html')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5079))
    app.run(host='0.0.0.0', port=port)

    


