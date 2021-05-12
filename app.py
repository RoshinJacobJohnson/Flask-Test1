import base64
from flask import Flask, request, jsonify
import numpy as np
import cv2





# Initialize the app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


class InvalidException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def __str__(self):
        return self.message

# route http posts to this method
@app.route("/api/face", methods=['POST'])
def detect_face():
    try:
        req = request.json

        if req.get('image') is None:
            raise InvalidException('image is required.')
            
        if req.get('size') is None:
            raise InvalidException('size is required.')

        # decode base64 string into np array
        nparr = np.frombuffer(base64.b64decode(req['image'].encode('utf-8')), np.uint8)

        # decoded image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise InvalidException('Unable to parse the image.')

        #num, data = img
        response = {
            'success': True,
            'status code': 201,
            'message': '{} faces detected'.format(num),
            'data': {'length': data},
            }
        resp = jsonify(response)
        resp.status_code = 200
        return resp

    except Exception as e:
        response = {
            'success': False,
            'status code': 500,
            'message': str(e),
            }
        resp = jsonify(response)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    app.run()
