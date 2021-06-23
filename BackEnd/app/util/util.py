from flask import jsonify, make_response
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError
from app.assets.request_message_map import *
from werkzeug.exceptions import BadRequest
from PIL import Image, UnidentifiedImageError
import json
import os
from inflection import underscore
from app.util.env_setup import set_google_cred
import urllib.request
from datetime import datetime



def generate_response(elem={}, status_code=200):
    """Simple wrapper to return consumable json response"""
    # generated response in default has 200 status code
    response = make_response(jsonify(elem), status_code)
    return response

def generate_message(message, status_code=200):
    """Use generate_response to for simple response with only a message entry"""
    json_response = {"message": message}
    return generate_response(json_response, status_code)


def is_loggedin(curr_session):
    """Check if the current user has already logged in"""
    access_token = curr_session.get("access_token", None)
    user_id = curr_session.get("user_id", None)
    # logged in is define by a accesstoken + an existing user_id
    # this prevents case where user doesn't create an account
    return access_token is not None and user_id is not None


def get_email_domain(email_string):
    """Get domain of an email string, assuming it is correctly formatted"""
    res = email_string.split('@')[-1]
    return res


def fetch_test_token(target_audience):
    """
    Fetch test token from a given service account

    verify with:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    return: (success, token)
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    except KeyError:
        # path not yet set
        set_google_cred()
    try:
        request = requests.Request()
        iden_token = id_token.fetch_id_token(
            request, target_audience)
        return True, iden_token
    except:
        return False, None


def verify_email(google_login_token, whitelisted_domains, target_audience):
    """
    Verify user email through Google Auth Token

    Token must satisfy the below criteria:
    1. the token is from a valid issuer
    2. the email domain is currently supported

    return: (status code, result message, the email)
    """
    MESSAGE_VERIFIED = "email is verified. So you are our HOMIE! NOICE"
    MESSAGE_NOT_SUPPORTED = "the domain is not currently supported. We will keep expanding."
    MESSAGE_INVALID_TOKEN = "The token is invalid. Seems like you want to be a con artist. Have you read the Art of Deception?"
    try:
        # first step, verify the token indeeds comes from GAuth
        request = requests.Request()
        id_info = id_token.verify_oauth2_token(
            google_login_token, request, target_audience)
        # second step, verify the email domain is whitelisted
        domain = get_email_domain(id_info['email'])
        if domain in whitelisted_domains:
            return 200, MESSAGE_VERIFIED, id_info['email']
        else:
            return 503, MESSAGE_NOT_SUPPORTED, id_info['email']
    except (GoogleAuthError, ValueError):
        return 401, MESSAGE_INVALID_TOKEN, None

def get_type_map(base,mode="write"):
    """
    Get a map between database entry name and its corresponding python types

    mode supports write and read
    
    If write, this also checks whether the keys are allowed as set in __user_write_permission_field__ of the base
    If read, this checks __user_read_permission_field__ 
    """
    check_fields = base.__user_write_permission_field__ if mode == "write" else base.__user_read_permission_field__
    # Get the db table column names and their corresponding python types
    type_map = {c.name: c.type.python_type for c in base.__table__.c if c.name in check_fields}
    return type_map

def get_valid_request_keys(keys, type_map):
    """
    Get the valid keys that match database schema in json from requests 

    Simply put: filter out all the json entries that aren't in the databse schema
    return (set of keys that contain the existing columns in both request json and database schema)
    """
    return set(key for key in keys if key in type_map)


def verify_request_datatype(valid_keys,name_val_dict, type_map):
    """
    Assumption: it assumes all the keys should be matched with those on the base
    Verify that the request json user submitted has the correct types defined in the database schema
    base is the data model we defined in the database setup
    return (whether all the data are correctly formatted, key value pair if correctly formatted)
    """
    valid_dict = {key:value for key, value in name_val_dict.items() if key in valid_keys}
    # has to be non-empty dict
    correct_format = all(isinstance(value, type_map[key]) for key,value in valid_dict.items()) and len(valid_dict) > 0
    return correct_format,valid_dict

def verify_authentication(client_token, login_session):
    """
    Verify the identity of users when they perform sensitive request such as POST
    Return true if verified, and false with the error response
    """
    # verify the token
    if client_token != login_session["access_token"]:
        return False,generate_message(MESSAGE_INVALID_TOKEN,401)
    return True, None

def check_verify_token(request,login_session):
    """
    Check the existence of the token and verify the validity of the token

    return (check status, response)
    """
    try:
        client_token = request.cookies["access_token"]
        # verify the token
        verified,response = verify_authentication(client_token,login_session)
        if verified == False: return False,response
    except KeyError:
        # access_token doesn't exist: user hasn't been authorized to create an entry in the db
        response = generate_message(MESSAGE_NO_ACCESS_TOKEN,401)
        return False, response
    # if successfully checked, return true, None(indicating to proceed next actions)
    return True, None

def convert_to_underscore(json_form):
    """
    Convert all the keys from camelCase to underscore case (snake_case)
    """
    new_json = {underscore(key):value for key,value in json_form.items()}
    return new_json

def check_json_form(request, bad_req_message, no_json_message):
    """
    Check the existence of JSON before actually processing the data
    return (check status, response, json_form)
    """
    try:
        requested_json = request.json
    except BadRequest:
        response = generate_message(bad_req_message,400)
        return False,response, None
    if requested_json is None:
        response = generate_message(no_json_message,400)
        return False, response, None

    new_json = convert_to_underscore(requested_json)
    return True, None, new_json

def transform_json_underscore(json_form):
    new_json = {underscore(key):value for key,value in json_form.items()}
    return new_json

def check_multi_form_json(request):
    """
    Check the existence of JSON sent through multi form request(which cannot be fetched by request.json) before actually processing the data
    return (check status, response, json_form)
    """
    try:
        requested_json = json.loads(request.form["json"])
    except KeyError:
        response = generate_message(MESSAGE_MULTI_FORM_NO_JSON,400)
        return False,response, None
    except json.decoder.JSONDecodeError:
        response = generate_message(MESSAGE_MULTI_FORM_JSON_DECODE_ERROR,400)
        return False,response, None
    if isinstance(requested_json,dict) != True:
        response = generate_message(MESSAGE_MULTI_FORM_INVALID_JSON + " : json isn't a dict.",400)
        return False,response, None
    elif len(requested_json) == 0:
        response = generate_message(MESSAGE_MULTI_FORM_EMPTY_JSON,400)
        return False,response, None
    # if json is invalid, transform the key names from js native to python native
    new_json = transform_json_underscore(requested_json)
    return True, None, new_json

def process_request_json(base,value_pairs, strict_mode=False, original=False, access_mode="write", nondb_type_map={}):
    """
    wrapper to process db related request json
    original determines whether return only valid key value pairs or the original unprocessed json
    if strict_mode is on, all keys in the db must be provided. This is helpful when user creates an entry rather than update it
    return (whether the json is in correct format, updates dictionary, error response)
    """
    type_map = get_type_map(base,access_mode)
    type_map.update(nondb_type_map)
    # if there are non db related keys in extra_keys, check them as well
    valid_keys = get_valid_request_keys(value_pairs.keys(),type_map)
    if strict_mode and len(valid_keys) != len(type_map):
        return False, None, generate_message(MESSAGE_INCOMPLETE_JSON,422)
    # verify the json data types
    correct_format,valid_value_pairs = verify_request_datatype(valid_keys,value_pairs,type_map)
    response = None if correct_format else generate_message(MESSAGE_WRONG_TYPE_JSON,422)
    return correct_format,value_pairs if original else valid_value_pairs, response

def verify_image(upload_file):
    """
    verify whether a file object is valid
    disclaimer: the imghdr what method might not work all the time for all images

    return format if valid, and the file object 
    """
    try:
        # see if we can open an image
        img = Image.open(upload_file)
        upload_file.seek(0)
        try:
            # see if img is valid
            img.verify()
            return img.format
        except Exception:
            return "error"
    except UnidentifiedImageError:
        return "error"

def check_attributes_str(value_pairs):
    """
    verify attributes exist in the request form and all attributes are strings
    assume value pairs is a dict

    return (whether the json is in correct format, value_pairs if correct, error response)
    """
    other_type = "other"
    facility_type = "facilities"
    if other_type not in value_pairs or facility_type not in value_pairs:
        return False, None, generate_message(MESSAGE_INCOMPLETE_JSON,422)
    if not isinstance(value_pairs[other_type],list) or not isinstance(value_pairs[facility_type],list):
        return False, None, generate_message(MESSAGE_WRONG_TYPE_JSON,422)
    for elem in value_pairs[other_type]:
        if not isinstance(elem,str): return False, None, generate_message(MESSAGE_WRONG_TYPE_JSON+"other types contain wrong type data",422)
    for elem in value_pairs[facility_type]:
        if not isinstance(elem,str): return False, None, generate_message(MESSAGE_WRONG_TYPE_JSON+"facility types contain wrong type data",422)
    return True,value_pairs, None

def download_json_data(endpoint):
    """
    Download json data from a remote end point

    THIS NEEDS TO UNIT TESTED and error handle more specifically
    """
    try:
        with urllib.request.urlopen(endpoint) as url:
            json_data = json.loads(url.read().decode())
    except:
        json_data = []
    return json_data

def set_landlord_data(app,aws_landlord_endpoint):
    landlord_data = download_json_data(aws_landlord_endpoint)
    landlord_data.sort(key=lambda elem: datetime.now() if elem['availability'].lower() == ["today","now"] else datetime.strptime(elem['availability'],'%m/%d/%Y'))
    app.config["LANDLORD_DB"] = landlord_data

def generate_user_login_data(user,test=False):
    user_prefix = "test_user" if test else "user"
    photo_path_name = "/".join([user_prefix+str(user.id),
                                "profile", "headshot.jpg"])
    json_response = {"name": user.name,
                     "email": user.email,
                     "message": MESSAGE_SUCCESS_LOGIN,
                     "description": user.description,
                     "phone": user.phone,
                     "schoolYear": user.school_year,
                     "major": user.major,
                     "profilePhoto": photo_path_name
                     }
    return json_response