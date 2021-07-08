import json
from flask import session
from app.util.util import *
from app.assets.request_message_map import *
import app.util.aws.s3 as s3
import pytest

@pytest.mark.parametrize(
    ("email", "user_id", "correct_response"),
    (
        # case 1: Testing existing user.
        # phone, description, schoolYear, major are attributes that already exist.
        # So they are used to compared the ones in the database rather than create new ones
        (
            "haha@ucsd.edu",
            1,
            {"name": "cris",
             "email": "haha@ucsd.edu",
             "phone": "858-911-1198",
             "description": "I recently graduated with my bachelor's and will be working/volunteering fulltime. I do not smoke and I am clean (might misplace things though but)! I am also very sociable and enjoy cooking and baking 🙂 Hobbies I have are playing the violin, drawing, and watching kdramas! Feel free to message me for further questions ",
             "schoolYear": "Third",
             "message": MESSAGE_SUCCESS_LOGIN,
             "major": "Data Science"}),
        # case 2: new user
        (
            "yzuaxi@ucsd.edu",
            None,
            {"newUser": True}),
        # case 3: the google email and the request email are different
    ),
)
def test_single_login_valid_input(client, email, user_id, correct_response):
    """Test the login process of flask"""
    rv = client.post(
        "/login", data=json.dumps({"email": email}), content_type="application/json")
    response_data = json.loads(rv.data)
    assert rv.status_code == 200
    for key, value in correct_response.items():
        assert response_data[key] == value
    # check cookie is set properly
    cookie_map = {cookie.name: cookie.value for cookie in client.cookie_jar}
    # only include session cookie and access token
    assert len(cookie_map) == 2
    # has cookie accesstoken
    assert "access_token" in cookie_map
    # accesstoken equal to that of current session
    with client:
        # dummy path to submit http request and get the client session
        client.get("/")
        assert cookie_map["access_token"] == session["access_token"]
        assert user_id == session.get("user_id", None)


@pytest.mark.parametrize(
    ("email", "correct_response"),
    (
        # case 1: Testing existing user.
        # phone, description, schoolYear, major are attributes that already exist.
        # So they are used to compared the ones in the database rather than create new ones
        (
            "haha@ucsd.edu",
            [{"name": "cris",
              "email": "haha@ucsd.edu",
              "phone": "858-911-1198",
              "description": "I recently graduated with my bachelor's and will be working/volunteering fulltime. I do not smoke and I am clean (might misplace things though but)! I am also very sociable and enjoy cooking and baking 🙂 Hobbies I have are playing the violin, drawing, and watching kdramas! Feel free to message me for further questions ",
              "schoolYear": "Third",
              "message": MESSAGE_SUCCESS_LOGIN,
              "major": "Data Science"},
             {"message": "You have already logged in"},
                {"message": "You have already logged in"}
             ]),
        # case 2: new user
        (
            "yzuaxi@ucsd.edu",
            [{"newUser": True},
             {"newUser": True},
                {"newUser": True}
             ]),
    ),
)
def test_multiple_login_valid_input(client, email, correct_response):
    """Test case where user has attempted several logins"""
    rv = client.post(
        "/login", data=json.dumps({"email": email}), content_type="application/json")
    response_data = json.loads(rv.data)
    # TODO: this test can be shortened, can use a for loop
    assert rv.status_code == 200
    # first time, same as previous single atomic test
    for key, value in correct_response[0].items():
        assert response_data[key] == value
    # second and third time, be informed of already loggedin. Third time is used to verify state doesn't change.
    rv = client.post(
        "/login", data=json.dumps({"email": email}), content_type="application/json")
    response_data = json.loads(rv.data)
    assert rv.status_code == 200
    for key, value in correct_response[1].items():
        assert response_data[key] == value
    rv = client.post(
        "/login", data=json.dumps({"email": email}), content_type="application/json")
    response_data = json.loads(rv.data)
    assert rv.status_code == 200
    for key, value in correct_response[2].items():
        assert response_data[key] == value


@pytest.mark.parametrize(
    ("email", "allowed_origins", "correct_response", "correct_status_code"),
    (
        # case 1: origin forbidden. valid origin has already been tested through default setting in previous tests.
        (
            "haha@ucsd.edu",
            {"127.0.0.2"},
            {"message":MESSAGE_WRONG_ORIGIN},
            401),
    )
)
def test_login_invalid_origin(client, app, email, allowed_origins, correct_response, correct_status_code):
    app.config["ALLOWED_ORIGINS"] = allowed_origins
    rv = client.post(
        "/login", data=json.dumps({"email": email}), content_type="application/json")
    response_data = json.loads(rv.data)
    for key, value in correct_response.items():
        assert response_data[key] == value
    assert rv.status_code == correct_status_code


@pytest.mark.parametrize(
    ("json_query", "online_config", "correct_response",
     "correct_status_code", "fetch_token_true"),
    (
        # case 1: Testing request json without token
        ({"data": json.dumps({"name": "cris"}), "content_type": "application/json"},
         {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
         {"message": MESSAGE_LOGIN_NO_GTOKEN},
         400,
         False),
        # case 2: Testing request without json header but with token
        ({"data": json.dumps({"google_login_token": "lol"})},
         {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
         {"message": MESSAGE_LOGIN_NO_JSON},
         400,
         False),
        # case 3: Testing request without json and without data
        ({},
         {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
         {"message": MESSAGE_LOGIN_NO_JSON},
         400,
         False),
        # case 4: Testing an email that have a valid token but doesn't have allowed domains
        ({"data": {}, "content_type": "application/json"},
         {"ALLOWED_DOMAINS": {"ucsd.edu"}},
         {"message": "the domain is not currently supported. We will keep expanding."},
         503,
         True),
        # case 5: Testing an email that is whitelisted and has valid token
        ({"data": {}, "content_type": "application/json"},
         {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
         {"message": MESSAGE_LOGIN_NEW_USER},
         200,
         True),
        # case 6: Testing request with an invalid token
        ({"data": json.dumps({"google_login_token": "lol"}), "content_type": "application/json"},
         {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
         {"message": "The token is invalid. Seems like you want to be a con artist. Have you read the Art of Deception?"},
         401,
         False),

    ),
)
def test_login_online(client, app, json_query, online_config, correct_response, correct_status_code, fetch_token_true):
    app.config["OFFLINE_TESTING"] = False
    app.config.update(online_config)
    # online test tends to be flaky due to dependency on API. So we try 3 times before giving up.
    if fetch_token_true == True:
        for _ in range(3):
            fetch_status, google_login_token = fetch_test_token(
                app.config["GAUTH_AUDIENCE"])
            if fetch_status == True:
                break
        if fetch_status != True:
            print("Remote API isn't working. Maybe try again later.")
            return
        json_query["data"]["google_login_token"] = google_login_token
        json_query["data"] = json.dumps(json_query["data"])
    rv = client.post(
        "/login", **json_query)
    response_data = json.loads(rv.data)
    assert rv.status_code == correct_status_code
    for key, value in correct_response.items():
        assert response_data[key] == value


@pytest.mark.parametrize(
    ("email", "login_first", "corrupt_cookie",
     "correct_response", "correct_status_code"),
    (
        # case1: successful logout => token and user id deleted
        (
            "haha@ucsd.edu",
            True,
            False,
            {"message": "Successful Logout!"},
            200),
        # case2: already logout/never login(no token and user id) => test Idempotence
        (
            "haha@ucsd.edu",
            False,
            False,
            {"message": "You have already logged out!"},
            200),
        # case3: unsuccessful logout => wrong token when user is still logged in(forgery attack)
        (
            "haha@ucsd.edu",
            True,
            True,
            {"message":
                "Cross-Site Request Forgery (XSRF/CSRF) attacks huh? GOTCHA!"},
            401),
    )
)
def test_single_logout(client, login_first, corrupt_cookie, email, correct_response, correct_status_code):
    """Test the logout process of flask"""
    # if the tests requires previous log in, do it
    if login_first:
        client.post(
            "/login", data=json.dumps({"email": email}), content_type="application/json")
    if corrupt_cookie:
        # corrupt the client's cookie => to create you have to destroy
        cookie_map = {cookie.name: cookie for cookie in client.cookie_jar}
        cookie_map["access_token"].value = "fake token to see whether the engineer is dumb"
    rv = client.get("/logout")
    response_data = json.loads(rv.data)
    for key, value in correct_response.items():
        assert response_data[key] == value
    assert rv.status_code == correct_status_code
    # if return 200 status, check if the accesstoken is deleted in cookie
    if rv.status_code == 200:
        # check cookie is set properly
        cookie_map = {cookie.name: cookie.value for cookie in client.cookie_jar}
        # has cookie accesstoken
        assert "access_token" not in cookie_map
        # accesstoken doesn't exist in current session
        with client:
            # dummy path to submit http request and get the client session
            client.get("/")
            assert session.get("access_token", None) == None
            assert session.get("user_id", None) == None


@pytest.mark.parametrize(
    ("email", "login_first", "corrupt_cookie", "json_query",
     "correct_response", "correct_status_code"),
    (
        # case1: successfully create user => right token, already verified through email
        (
            "nonexistent@ucsd.edu",
            True,
            False,
            {"data": json.dumps({"name": "CRISTIANO",
                                 "email": "nonexistent@ucsd.edu",
                                 "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                                 "phone": "858-777-2345",
                                 "schoolYear": "Grad",
                                 "major": "MARVEL SCIENCE",
                                 }), "content_type": "application/json"},
            {"name": "CRISTIANO",
             "email": "nonexistent@ucsd.edu",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": "858-777-2345",
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      "profilePhoto": "test_user5/profile/headshot.jpg",
                      "message": "Welcome to be a new HOMIE! CONGRATS!"
             },
            201
        ),
        # case2: creation failure => invalid token
        (
            "nonexistent@ucsd.edu",
            True,
            True,
            {"data": json.dumps({"name": "CRISTIANO",
                                 "email": "nonexistent@ucsd.edu",
                                 "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                                 "phone": "858-777-2345",
                                 "schoolYear": "Grad",
                                 "major": "MARVEL SCIENCE",
                                 }), "content_type": "application/json"},
            {"message":
                "Cross-Site Request Forgery (XSRF/CSRF) attacks huh? GOTCHA!"},
            401
        ),
        # case3: creation failure => no token
        (
            "nonexistent@ucsd.edu",
            False,
            False,
            {"data": {"name": "CRISTIANO",
                      "email": "nonexistent@ucsd.edu",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": "858-777-2345",
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      }, "content_type": "application/json"},
            {"message":
             "Welcome to the Lost World: Jurassic Park. You are not authorized to create an entry here."},
            401
        ),
        # case4: creation reject => already exists
        (
            "haha@ucsd.edu",
            True,
            False,
            {"data": {"name": "CRISTIANO",
                      "email": "nonexistent@ucsd.edu",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": "858-777-2345",
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      }, "content_type": "application/json"},
            {"message":
             "Body double is not allowed. Should've gone for the head. "},
            405
        ),
        # case5: valid token and new user but register json isn't complete (most likely access without using frontend form)
        (
            "nonexistent@ucsd.edu",
            True,
            False,
            {"data": json.dumps({"name": "CRISTIANO",
                                 "email": "nonexistent@ucsd.edu",
                                 "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                                 "phone": "858-777-2345",
                                 "major": "MARVEL SCIENCE",
                                 "profilePhoto": "dummy.jpg"
                                 }), "content_type": "application/json"},
            {"message":
             "JSON is not complete. Did you bypass the frontend? How did you find us? SURPRISING PIKACHU FACE"},
            400
        ),
        # case6: valid token and new user but no json
        (
            "nonexistent@ucsd.edu",
            True,
            False,
            {"data": {}},
            {"message":
             "Why create users without a json? Did you forget something?"},
            400
        ),
        # case7: valid token and new user but ill-format json
        (
            "nonexistent@ucsd.edu",
            True,
            False,
            {"data": {"name": "CRISTIANO",
                      "email": "nonexistent@ucsd.edu",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": "858-777-2345",
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      }, "content_type": "application/json"},
            {"message": "Oops. Bad format for your json. Try again"
             },
            400
        ),
        # case8: invalid types for some entries
        (
            "nonexistent@ucsd.edu",
            True,
            False,
            {"data": json.dumps({"name": "CRISTIANO",
                      "email": "nonexistent@ucsd.edu",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": 123456,
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      }), "content_type": "application/json"},
            {"message":"the input data doesn't fit our schema. Did you bypass our frontend?"},
            422
        ),
    )
)
def test_create_user(client, email, login_first, corrupt_cookie, json_query, correct_response, correct_status_code):
    """ 
    Test the create user process
    prerequisite: 
    valid access token => email already verified (authentication)
    no user_id => not in the database => true new user (nonduplication)
    """
    # if the tests requires previous log in, do it
    if login_first:
        client.post(
            "/login", data=json.dumps({"email": email}), content_type="application/json")
    if corrupt_cookie:
        # corrupt the client's cookie => to create you have to destroy
        cookie_map = {cookie.name: cookie for cookie in client.cookie_jar}
        cookie_map["access_token"].value = "fake token to see whether the engineer is dumb"
    rv = client.post(
        "/createUser", **json_query)
    response_data = json.loads(rv.data)
    for key, value in correct_response.items():
        assert response_data[key] == value
    assert rv.status_code == correct_status_code

@pytest.mark.parametrize(
    ("login_first", "online_config","json_query", 
     "correct_response", "correct_status_code"),
    (
        # case1: successfully create user => right token, already verified through email
        (
            True,
            {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
            {"data": json.dumps({"name": "CRISTIANO",
                                 "email": "nonexistent@ucsd.edu",
                                 "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                                 "phone": "858-777-2345",
                                 "schoolYear": "Grad",
                                 "major": "MARVEL SCIENCE",
                                 }), "content_type": "application/json"},
            {"name": "CRISTIANO",
             "email": "homehubtest@homehub-312115.iam.gserviceaccount.com",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": "858-777-2345",
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      "profilePhoto": "test_user5/profile/headshot.jpg",
                      "message": "Welcome to be a new HOMIE! CONGRATS!"
             },
            201
        ),
        # case2: creation success => ignore invalid email
        (
            True,
            {"ALLOWED_DOMAINS": {"ucsd.edu", "homehub-312115.iam.gserviceaccount.com"}},
            {"data": json.dumps({"name": "CRISTIANO",
                                 "email": "nonexistent@ucsd.edu",
                                 "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                                 "phone": "858-777-2345",
                                 "schoolYear": "Grad",
                                 "major": "MARVEL SCIENCE",
                                 }), "content_type": "application/json"},
            {"name": "CRISTIANO",
             "email": "homehubtest@homehub-312115.iam.gserviceaccount.com",
                      "description": "YOU COULD NOT LIVE WITH YOUR OWN FAILURE, AND WHERE DID THAT BRING YOU? BACK TO ME",
                      "phone": "858-777-2345",
                      "schoolYear": "Grad",
                      "major": "MARVEL SCIENCE",
                      "profilePhoto": "test_user5/profile/headshot.jpg",
                      "message": "Welcome to be a new HOMIE! CONGRATS!"
             },
            201
        ),
    )
)
def test_create_user_online(app,client, login_first, online_config, json_query, correct_response, correct_status_code):
    """ 
    Test the create user process when the user is online
    """
    app.config["OFFLINE_TESTING"] = False
    app.config.update(online_config)
    for _ in range(3):
        fetch_status, google_login_token = fetch_test_token(
            app.config["GAUTH_AUDIENCE"])
        if fetch_status == True:
            break
    if fetch_status != True:
        print("Remote API isn't working. Maybe try again later.")
        return
    rv = client.post("/login", **{"data": json.dumps({"google_login_token":google_login_token}), "content_type": "application/json"})
    rv = client.post(
                "/createUser", **json_query)
    response_data = json.loads(rv.data)
    for key, value in correct_response.items():
        assert response_data[key] == value
    assert rv.status_code == correct_status_code
    profile_image_array = s3.get_images("test_user5",category="profile")
    assert len(profile_image_array) == 1
    assert profile_image_array[0] == "test_user5/profile/headshot.jpg"
    s3.delete_file_wname("test_user5/profile/headshot.jpg","houseit")
