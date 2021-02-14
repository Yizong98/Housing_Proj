from flask import current_app, Blueprint, request, \
    jsonify, session as login_session, Response
from app.db.crud import get_row_if_exists, add_user
from app.db.database_setup import User
from datetime import datetime
from app.util.util import generateResponse
from app.util.aws.s3 import upload_file_wname
import os
import random
import string

authetication = Blueprint('auth', __name__)


@authetication.route("/login", methods=['POST', 'OPTIONS'])
def login():
    """Create anti-forgery state token."""
    if request.method == 'OPTIONS':
        return generateResponse()
    access_token = "".join(random.choice(string.ascii_uppercase + string.digits)
                           for x in range(32))
    login_session["access_token"] = access_token
    requested_json = request.json
    # check in with db to see if user is new
    session = current_app.config['DB_CONNECTION']
    user = get_row_if_exists(User, session, **{'email': requested_json['email']})
    if not user:
        # User doesn't exist
        # maybe also do: , 'access_token': access_token
        json_response = {'newUser': True}
        response = generateResponse(json_response)
        response.set_cookie('access_token', access_token)
        return response
    path_name = "/".join(["user"+str(user.id),
                          'profile', "headshot.jpg"])
    login_session["user_id"] = user.id
    json_response = {'name': requested_json['name'],
                     'email': requested_json['email'],
                     'access_token': access_token,
                     'message': 'Successfully created room.',
                     'description': user.description,
                     'phone': user.phone,
                     'schoolYear': user.school_year,
                     'major': user.major,
                     'profile_photo': path_name
                     }
    response = generateResponse(json_response)
    response.set_cookie('access_token', access_token)
    return response


@authetication.route("/logout", methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return generateResponse()
    client_token = request.json.get('access_token')
    message, status = 'Successful Logout!', 200
    # delete the user id
    if not client_token or (client_token != login_session["access_token"]):
        message, status = 'Logout is Forbidden due to wrong token', 403
        print(client_token, login_session["access_token"])
    else:
        del login_session["user_id"]
    return generateResponse(elem=message, status=status)


@authetication.route("/createUser", methods=["POST", "OPTIONS"])
def create_user():
    session = current_app.config['DB_CONNECTION']
    if request.method == 'OPTIONS':
        return generateResponse()
    requested_json = request.json
    if get_row_if_exists(User, session, **{'email': requested_json['email']}):
        message, status = 'Already Created', 200
        return generateResponse(elem=message, status=status)

    user = add_user(requested_json['name'],
                    requested_json['email'],
                    datetime.now(),
                    requested_json['phone'],
                    requested_json["description"],
                    requested_json["schoolYear"],
                    requested_json["major"],
                    session)
    login_session["user_id"] = user.id
    icon_path = './assets/profile_default_icons/'
    selected_icon = random.choice(
        os.listdir(icon_path))
    path_name = "/".join(["user"+str(user.id),
                          'profile', "headshot.jpg"])
    upload_file_wname(icon_path+selected_icon, 'houseit', path_name)

    json_response = {'name': requested_json['name'],
                     'email': requested_json['email'],
                     'access_token': login_session["access_token"],
                     'message': 'Successfully created room.',
                     'description': user.description,
                     'phone': user.phone,
                     'schoolYear': user.school_year,
                     'major': user.major,
                     'profile_photo': path_name
                     }
    response = generateResponse(json_response, 201)
    response.set_cookie('access_token', login_session["access_token"])

    return response
