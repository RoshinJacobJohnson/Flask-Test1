#main.py

# Import the Flask module that has been installed.
from flask import Flask
from flask import jsonify,request

from get_measurements import measurements
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
    result=measurements(fitness,size)
    #result = {    'shirt-size': size }
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
