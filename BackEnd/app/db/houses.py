from database_setup import User, Room, Move_In, \
    House_Attribute, Attribute, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.util.aws.s3 import get_images
from crud import add_user, \
    add_room, add_move_in, add_house_attribute, add_attribute
import os

password = os.environ["DBPASSWORD"]
engine = create_engine(
    'mysql://admin:{password}@homehubdb.cluster-cdmngikujtht.us-east-2.rds.amazonaws.com:3306/housing'.format(password=password))
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# define constants
CRIS = "cris"
AMIT = "amit"
ADAM = "adam"
KEENAN = "keenan"

# Add mock users
cris = add_user(CRIS, "haha@ucsd.edu", datetime.now(), "858-911",
                "yo I am Cris. P dope. DAMNNNNNNNNNNNN", 'Senior',
                "Data Science", session)
amit = add_user(AMIT, "amit@ucsd.edu", datetime.now(), "858-911989",
                "yo I am Amit. P dope. DAMNNNNNNNNNNNN",  'Senior',
                "Data Science", session)
adam = add_user(ADAM, "adam@ucsd.edu", datetime.now(), "858-65386",
                "yo I am Adam. P dope. ADAMNNNNNNNNN. YOOOOOOO", 'Senior',
                "Computer Science and Engineering",
                session)
keenan = add_user(KEENAN, "keenan@ucsd.edu", datetime.now(), "858-4675432",
                  "yo I am Keenan. P dope. DAMNNNNNNNNNNNN. YOOOOOOO",  'Grad',
                  "Computer Science and Engineering",
                  session)
# Add mock Move-in
cris_move_in = add_move_in("Anytime", "September",
                           "Late(21-31)", "September", session)
amit_move_in = add_move_in(
    "Anytime", "January", "Late(21-31)", "September", session)
keenan_move_in = add_move_in(
    "Anytime", "January", "Late(21-31)", "March", session)
adam_move_in = add_move_in(
    "Anytime", "January", "Late(21-31)", "October", session)

# Add mock Attribute
attr_gym = add_attribute('gym room', 'facilities', session)
attr_park = add_attribute('parking', 'facilities', session)
attr_ele = add_attribute('elevator', 'facilities', session)
attr_male = add_attribute('male', 'other', session)
attr_pri = add_attribute('private', 'other', session)
attr_female = add_attribute('female', 'other', session)

# Add Room
cris_room = add_room(datetime.now(), "single", 1000, "Damn it LOOOOOOL", 2,
                     "16 mins",
                     "Costa Verde Village, Costa Verde Boulevard, San Diego, CA, USA",
                     cris, cris_move_in, session)
amit_room = add_room(datetime.now(), "single", 2000, "Damn it LOOOOOOL", 10,
                     "5 mins",
                     "Solazzo Apartment Homes, Villa La Jolla Drive, La Jolla, CA, USA",
                     amit, amit_move_in, session)
keenan_room = add_room(datetime.now(), "single", 3000, "Damn it LOOOOOOL", 5,
                       "65 mins",
                       "Regents Court, Regents Road, San Diego, CA, USA",
                       keenan, keenan_move_in, session)
adam_room = add_room(datetime.now(), "livingRoom", 5000, "Damn it LOOOOOOL", 9,
                     "60 mins",
                     "Towers At Costa Verde, Costa Verde Boulevard, San Diego, CA, USA",
                     adam, adam_move_in, session)

# Add House_Attribute
add_house_attribute(cris_room, attr_gym, session)
add_house_attribute(cris_room, attr_park, session)
add_house_attribute(cris_room, attr_male, session)
add_house_attribute(amit_room, attr_gym, session)
add_house_attribute(amit_room, attr_ele, session)
add_house_attribute(amit_room, attr_park, session)
add_house_attribute(keenan_room, attr_male, session)
add_house_attribute(keenan_room, attr_ele, session)
add_house_attribute(keenan_room, attr_park, session)
add_house_attribute(keenan_room, attr_pri, session)
add_house_attribute(adam_room, attr_female, session)
add_house_attribute(adam_room, attr_ele, session)
add_house_attribute(adam_room, attr_park, session)
add_house_attribute(adam_room, attr_pri, session)

print("created Mock Database!")