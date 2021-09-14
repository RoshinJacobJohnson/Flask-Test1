#main.py

# Import the Flask module that has been installed.
from flask import Flask
from flask import jsonify,request
import base64
from get_measurements import measurements
import image_measurements
# Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
app = Flask(__name__)




@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    return jsonify({'sum': data['a'] + data['b']})



@app.route('/predict', methods=['POST'])
def predict():
    #data = request.get_json()
    #data=request.data
    #data=request.args
    #size=request.form['size']
    #size=data['size']
    data = request.get_json()
    size=data["size"]
    fitness=data["fitness"]
    imageString = base64.b64decode(data['img'])
    try:
        chest,waist, hip, cuffs= image_measurements.measure(imageString)
    except:
        chest,waist, hip, cuffs=0,0,0,0
    
    
    #image_b=data["image_as_base64"]
    #image_bytes=base64.decodebytes(image_b)
    result=measurements(fitness,size)
    #return data.keys()
    if(abs(result["chest"]-chest)<1.6):
        result["chest"]=chest
      
    if(abs(result["waist"]-waist)<2):
        result["waist"]=waist
    if(abs(result["hip"]-hip)<2):
        result["hip"]=hip
        
    if(abs(result["cuffs"]-cuffs)<0.4):
        result["cuffs"]=cuffs
    return jsonify(result)


@app.route('/predictdefault', methods=['POST'])
def predictdefault():
    #data = request.get_json()
    #data=request.data
    #data=request.args
    #size=request.form['size']
    #size=data['size']
    data = request.get_json()
    size=data["size"]
    fitness=data["fitness"]
    result=measurements(fitness,size)
    #return data.keys()
    
    return jsonify(result)
    #return "Testing"


# Annotation that allows the function to be hit at the specific URL.
@app.route("/")
# Generic Python functino that returns "Hello world!"
def index():
    return "Hello world!"





@app.route('/ping', methods=['GET'])
def ping():
    return "Pinging Model!!"


# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
    # Runs the Flask application only if the main.py file is being run.
    app.debug = True
    app.run()
