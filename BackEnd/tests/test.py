from app.util.search import search
from app.db.database_setup import Base, User
from app.db.crud import write_room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
engine = create_engine('mysql:///../app/db/housing.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def testSearch():
    testRoomJson = {'distance': '70 mins', 'room_type': ['livingRoom'], 'price_min': 200, 'price_max': 6000,
                    'early_interval': 'Anytime', 'early_month': 'January', 'late_interval': 'Early', 'late_month': 'September', 'stay_period': 9,
                    'other': ['female'], 'facilities': ['parking']
                    }
    return search(testRoomJson, session)


# print(testSearch())


def testPost():
    imgs_path = os.listdir('.')
    photos = [open(path, "rb")
              for path in imgs_path if path.endswith("jpg")]
    testRoomJson = {'distance': '30 mins', 'room_type': 'livingRoom', 'price': 5000,
                    'early_interval': 'Anytime', 'early_month': 'January', 'late_interval': 'Early', 'late_month': 'September', 'stay_period': 9,
                    'other': ['male'], 'facilities': ['parking'], 'address': 'Village Square Apartments, Via Mallorca, La Jolla, CA, USA',
                    'name': 'Ali', 'leaserEmail': 'yixi@ucsd.edu', 'leaserPhone': '', 'roomDescription': 'happy person happy life', 'leaserSchoolYear': 3,
                    'leaserMajor': 'Cogs HCI', 'description': 'P DOPE PLACE. TRY IT',
                    'photo': photos
                    }
    for p in photos:
        print(p.name)
    write_room(testRoomJson, session)
