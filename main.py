
from flask import Flask, jsonify, request
from service import get_weather, get_download_progress
import argparse
app = Flask("API_Weather")
API_KEY = ''
class InvalidAPIUsage(Exception):
    status_code = 400
    def __init__(
        self, message : str, status_code : int =None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code
@app.route('/')
def index():
    return jsonify({'message': 'Welcome!'})

@app.route('/weather/', methods=['POST'])
def post_weather():
    """
    Function that get the weather for the list of cities' ids
    Args:
        body:
            {
                'id_user' : 'unique string value'
            }
    """
    data = request.json
    if 'user_id' in data:
        user_id = data['user_id']
        return jsonify(
            get_weather(user_id=user_id, api_key=API_KEY))
    else:
        print("ERROR!")
        raise InvalidAPIUsage(
            "The body have to have the format:\
                {'id_user' : 'value'}",
            status_code=422)

@app.route('/download/progress/<id_user>', methods=['GET'])
async def get_progress(id_user):
    """
    Function that call other in order to get the download's progress
    Args:
        id_user (str) : the id bring by the user for his own query.
            It´s must be unque.    
    """
    return jsonify(get_download_progress(id_user))

if __name__ == '__main__':
    """
    When the sscript is invoqued, the user must to add his API KEY
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apikey", help="Open API Weather KEY")
    args = parser.parse_args()
    API_KEY = args.apikey
    app.run(host='0.0.0.0',debug=True, port=8585)