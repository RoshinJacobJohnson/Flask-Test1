#main.py

# Import the Flask module that has been installed.
from flask import Flask

# Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
app = Flask(__name__)




@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    return jsonify({'sum': data['a'] + data['b']})





@app.route('/predict', methods=['POST'])
def predict():
    vehicle = request.get_json()


    result = {
        'mpg_prediction': 23
    }
    return jsonify(result)



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
