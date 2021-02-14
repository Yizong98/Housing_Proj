from database_setup import User, Room, Move_In, \
    House_Attribute, Attribute, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.util.aws.s3 import get_images, upload_file_wname
from app.assets.options import months, intervals, others, facilities, school_years, room_types, addresses_generate
from crud import add_user, \
    add_room, add_move_in, add_house_attribute, add_attribute
import os
import random


engine = create_engine('sqlite:///housing.db')
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

descriptions = {
    CRIS: "I recently graduated with my bachelor's and will be working/volunteering fulltime. I do not smoke and I am clean (might misplace things though but)! I am also very sociable and enjoy cooking and baking 🙂 Hobbies I have are playing the violin, drawing, and watching kdramas! Feel free to message me for further questions ",
    AMIT: "We are pretty chill and very neat and respectful people ",
    ADAM: "Studying Data Science and Mathematics at the University of California, San Diego. Well-versed in Python (SKLearn, Pandas, Dask, etc..), R and Excel.Looking for an internship from June 2021 to September 2021 in the field of Data Science/Analytics where I can combine my mathematical/statistical knowledge and programming abilities with my strong writing and communication skills. ",
    KEENAN: "Software engineer with an attention to detail and strong people skills. Seeking full-time Software Engineering positions. "
}

# Add mock users
cris = add_user(CRIS, "haha@ucsd.edu", datetime.now(), "858-911",
                descriptions[CRIS], 'Third',
                "Data Science", session)
amit = add_user(AMIT, "amit@ucsd.edu", datetime.now(), "858-911989",
                descriptions[AMIT],  'Third',
                "Data Science", session)
adam = add_user(ADAM, "adam@ucsd.edu", datetime.now(), "858-65386",
                descriptions[ADAM], 'Third',
                "Computer Science and Engineering",
                session)
keenan = add_user(KEENAN, "keenan@ucsd.edu", datetime.now(), "858-4675432",
                  descriptions[KEENAN],  'Grad',
                  "Computer Science and Engineering",
                  session)
users = [adam, cris, amit, keenan]
file_dir = '../assets/room_mock_images/'
for user in users:
    # create icons
    icon_path = '../assets/profile_default_icons/'
    selected_icon = random.choice(
        os.listdir(icon_path))
    path_name = "/".join(["user"+str(user.id),
                          'profile', "headshot.jpg"])
    upload_file_wname(icon_path+selected_icon, 'houseit', path_name)


def generateMock(k=30):
    attributes = []
    for attr in others:
        attributes.append(add_attribute(attr, 'other', session))
    for attr in facilities:
        attributes.append(add_attribute(attr, 'facilities', session))
    move_combos = [(random.choice(intervals), months[6],
                    random.choice(intervals), months[7]) for _ in range(k)]
    move_ins = [add_move_in(elem[0], elem[1], elem[2],
                            elem[3], session) for elem in move_combos]
    mock_room_types = [random.choice(room_types) for _ in range(k)]
    mock_prices = [random.randint(200, 1000) for _ in range(k)]
    houses = [random.choice(addresses_generate) for _ in range(k)]
    people = [users[i % len(users)] for i in range(k)]
    negotiables = [random.choice([True, False]) for _ in range(k)]
    mock_stay_periods = [random.choice(list(range(1, 13))) for _ in range(k)]
    mock_eta = [str(random.choice(list(range(1, 30)))) +
                " mins" for _ in range(k)]
    mock_baths = [random.choice(list(range(1, 4))) for _ in range(k)]
    mock_beds = [random.choice(list(range(1, 4))) for _ in range(k)]
    mock_attrs = [list(set(random.sample(attributes, 8))) for _ in range(k)]
    mock_rooms = []
    print(mock_room_types)
    for i in range(k):
        temp_room = add_room(datetime.now(), mock_room_types[i], mock_prices[i], negotiables[i], "Damn it LOOOOOOL", mock_stay_periods[i],
                             mock_eta[i],
                             houses[i],
                             people[i], move_ins[i], mock_beds[i], mock_baths[i], session)
        for temp_attr in mock_attrs[i]:
            add_house_attribute(temp_room, temp_attr, session)
        mock_rooms.append(temp_room)
    for i in range(k):
        path_name = "/".join(["user"+str(people[i].id), 'housing',
                              str(mock_rooms[i].id)])
        random_files = random.sample(os.listdir(file_dir), 4)
        for idx, file_name in enumerate(random_files):
            upload_file_wname(file_dir+file_name, 'houseit',
                              path_name+"/"+str(idx)+".jpg")


generateMock()
print("created Mock Database!")
