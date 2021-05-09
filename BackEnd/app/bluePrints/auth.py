from flask import current_app, Blueprint, request, \
    jsonify, session as login_session, Response
from app.db.crud import get_row_if_exists, add_user
from app.db.database_setup import User
from datetime import datetime
from app.util.util import *
from app.assets.request_message_map import *
from app.util.aws.s3 import upload_file_wname
import os
import random
import string
from crud import *

authetication = Blueprint("auth", __name__)


@authetication.route("/login", methods=["POST", "OPTIONS"])
def login():
    """Login function and create anti-forgery state token."""
    # PART1: Secure measure to verify identity
    # first check if the domain is allowed
    if request.remote_addr not in current_app.config["ALLOWED_ORIGINS"]:
        print('IM HERE YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO WHATS UP')
        response = generate_message(MESSAGE_WRONG_ORIGIN,401)
        return response
    # pre-flight for CORS communication
    if request.method == "OPTIONS":
        return generate_response()
    # if user has already logged in, tell them
    if is_loggedin(login_session):
        response = generate_message(MESSAGE_ALREADY_LOGIN)
        return response
    # check requested json, see if the json contains required login info
    # first check if json exists from request
    checked_json, response, requested_json = check_json_form(request,MESSAGE_BAD_JSON,MESSAGE_LOGIN_NO_JSON)
    if checked_json != True: return response
    # second check if json conatins enough info
    try:
        google_login_token = requested_json["googleLoginToken"]
        # check if json contains valid info(ucsd email and google auth token)
        status_code, message, user_email = verify_email(
            google_login_token, current_app.config["ALLOWED_DOMAINS"], current_app.config["GAUTH_AUDIENCE"])
        # if not valid, troll them(very likely to be a hacker)
        if status_code != 200:
            response = generate_message(message,status_code)
            return response
    except KeyError:
        # if in online test mode or production mode, return invalid response
        if current_app.config["OFFLINE_TESTING"] != True:
            response = generate_message(MESSAGE_LOGIN_NO_GTOKEN,400)
            return response
        user_email = requested_json["email"]
        # else just continue the flow for offline testing
    # this is needed to ensure the email loaded eventually to the database is valid, if user continues to create an account
    login_session["login_user_email"] = user_email

    # PART2: Check whether user is new and return corresponding response
    # access token will be issued only after user's identity is verified
    access_token = "".join(random.choice(string.ascii_uppercase + string.digits)
                           for x in range(32))
    login_session["access_token"] = access_token
    # check in with db to see if user is new
    session = current_app.config["DB_CONNECTION"]
    # Assumption: user email is a unique identifier
    user = get_row_if_exists(
        User, session, **{"email": user_email})
    if not user:
        # User doesn't exist
        json_response = {"newUser": True, "message": MESSAGE_LOGIN_NEW_USER}
        response = generate_response(json_response)
        response.set_cookie("access_token", access_token)
        return response
    photo_path_name = "/".join(["user"+str(user.id),
                                "profile", "headshot.jpg"])
    login_session["user_id"] = user.id
    json_response = {"name": user.name,
                     "email": user_email,
                     "message": MESSAGE_SUCCESS_LOGIN,
                     "description": user.description,
                     "phone": user.phone,
                     "schoolYear": user.school_year,
                     "major": user.major,
                     "profile_photo": photo_path_name
                     }
    response = generate_response(json_response)
    response.set_cookie("access_token", access_token)
    return response


@authetication.route("/logout", methods=["GET"])
def logout():
    """Log out the user by verifying the token"""
    try:
        # try to get the access token possibly stored in the user's request
        client_token = request.cookies["access_token"]
        # verify the token
        verified,response = verify_authentication(client_token,login_session)
        if verified == False: return response
        # token verified, login successful
        # delete the token cookie during log out and user info in the backend
        del login_session["user_id"]
        del login_session["access_token"]
        response = generate_message(MESSAGE_SUCCESS_LOGOUT)
        response.delete_cookie("access_token")
    except KeyError:
        # access_token doesn't exist: either logged out already or never logged in
        response = generate_message(MESSAGE_ALREADY_LOGOUT)
    return response

@authetication.route("/createUser", methods=["POST", "OPTIONS"])
def create_user():
    """Create user function that is called when user is not in the database"""
    # handle pre-flight for browsers CORS access
    if request.method == "OPTIONS":
        return generate_response()

    # part1: verify that the request is legit
    session = current_app.config["DB_CONNECTION"]
    # verify the token
    checked_and_verified, response = check_verify_token(request,login_session)
    if checked_and_verified == False: return response
    try:
        # if some existing users are techie, troll them
        user_id = login_session["user_id"]
        response = generate_message(MESSAGE_CREATE_USER_DUPLICATE_REQUEST,405)
        return response
    except KeyError:
        # nice error. This means we can proceed to process their json
        checked_json, response, requested_json = check_json_form(request,MESSAGE_BAD_JSON,MESSAGE_CREATE_USER_NO_JSON)
        if checked_json == False: return response
        try:
            user_name = requested_json["name"]
            # user must complete account creation in the same session
            # no need to handle key error since til now the login_user_email should exist
            user_email = login_session["login_user_email"]
            user_phone = requested_json["phone"]
            user_description = requested_json["description"]
            user_school_year = requested_json["schoolYear"]
            user_major = requested_json["major"]
            # verify types
            correct_format,valid_update_pairs, response = process_request_json(User,
            {"name":user_name,
            "email":user_email,
            "phone":user_phone,
            "description":user_description,
            "school_year":user_school_year,
            "major":user_major})
            if correct_format == False: return response
            user = add_user(user_name,
                            user_email,
                            datetime.now(),
                            user_phone,
                            user_description,
                            user_school_year,
                            user_major,
                            session)
            # update the user id in the session
            login_session["user_id"] = user.id
            # cris's favorite part: create randome icons
            icon_path = "app/assets/profile_default_icons/"
            selected_icon = random.choice(
                os.listdir(icon_path))
            photo_path_name = "/".join(["user"+str(user.id),
                                        "profile", "headshot.jpg"])
            #  upload the image to S3 endpoint if not offline testing
            if current_app.config["OFFLINE_TESTING"] != True:
                upload_file_wname(icon_path+selected_icon,
                                  "houseit", photo_path_name)
            # finally, send the sensitive data to be displayed on frontend/some techie user
            json_response = {"name": user_name,
                             "email": user_email,
                             "message": "Welcome to be a new HOMIE! CONGRATS!",
                             "description": user_description,
                             "phone": user_phone,
                             "schoolYear": user_school_year,
                             "major": user_major,
                             "profile_photo": photo_path_name
                             }
            status_code = 201
            response = generate_response(json_response, status_code)
            return response
        except KeyError:
            response = generate_message(MESSAGE_CREATE_USER_INCOMPLETE_JSON,400)
            return response
