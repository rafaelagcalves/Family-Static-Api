"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def create_member():
    body = request.get_json()
    new_member = {
        "id" : body.get("id"),
        "first_name" : body.get("first_name"),
        "last_name" : body.get("last_name"),
        "age" : body.get("age"),
        "lucky_numbers": body.get("lucky_numbers")
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member)


@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    user = jackson_family.get_member(id)
    if user:
        return user, 200
    return 404

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    user = jackson_family.delete_member(id)
    if user:
        return jsonify({"done": True}), 200
    return 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
