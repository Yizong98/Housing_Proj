from app.db.database_setup import User, Room, Move_In,\
    House_Attribute, Attribute, Bookmark, Address, Stay_Period, Base
from app.util.aws.s3 import get_images, upload_file_wobject
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOUSEIT_S3_URL = 'https://houseit.s3.us-east-2.amazonaws.com/'

# Helper fns


def getSession(db_path):
    """
    get a given db session
    """
    engine = create_engine(db_path)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def add_and_commit(db_row, session):
    session.add(db_row)
    session.commit()

# Create

def add_user(name, email, date_created, phone, description, school_year, major,
             session):
    '''
    add a row to the User table
    '''
    User_to_add = User(name=name, email=email, date_created=date_created,
                       phone=phone, description=description,
                       school_year=school_year,
                       major=major)
    add_and_commit(User_to_add, session)
    return User_to_add

def add_address(distance, address, session):
    '''
    add a row to the Address table
    '''
    address_to_add = Address(address=address, distance=distance)
    add_and_commit(address_to_add, session)
    return address_to_add


def add_address(distance, address, session):
    '''
    add a row to the Address table
    '''
    address_to_add = Address(address=address, distance=distance)
    add_and_commit(address_to_add, session)
    return address_to_add


def add_room(date_created, room_type, price, negotiable, description,
             stay_period, address,
             user, move_in, no_rooms, no_bathrooms,
             session):
    '''
    add a row to the Room table
    '''
    Room_to_add = Room(date_created=date_created, room_type=room_type,
                       price=price,
                       negotiable=negotiable,
                       description=description, stay_period=stay_period,
                       address=address,
                       user=user, move_in=move_in, no_rooms=no_rooms,
                       no_bathrooms=no_bathrooms)
    add_and_commit(Room_to_add, session)
    return Room_to_add


def add_move_in(early_date, late_date, session):
    '''
    add a row to the Move_In table
    '''
    Move_In_to_add = Move_In(early_date=early_date,
                             late_date=late_date)
    add_and_commit(Move_In_to_add, session)
    return Move_In_to_add


def add_stay_period(from_month, to_month, session):
    '''
    add a row to the Stay_Period table
    '''
    Stay_Period_to_add = Stay_Period(from_month=from_month,
                                     to_month=to_month)
    add_and_commit(Stay_Period_to_add, session)
    return Stay_Period_to_add


def add_house_attribute(room, house_attribute, session):
    '''
    link attribute to an associated room_id if
    the link isn't already present
    links are recorded in the House_Attribute table
    attributes are recorded in the Attribute table
    '''
    house_attribute_to_add = get_row_if_exists(
        House_Attribute, session, ** {'room_id': room.id,
                                      'attribute_name': house_attribute.name})
    if not house_attribute_to_add:
        house_attribute_to_add = House_Attribute(
            room=room, house_attribute=house_attribute)
        add_and_commit(house_attribute_to_add, session)
    return house_attribute_to_add


def add_attribute(name, category, session):
    '''
    add an attribute to the Attribute table
    if it doesn't already exist there
    '''
    attribute_to_add = get_row_if_exists(Attribute, session, **
                                         {'name': name, 'category': category})
    if not attribute_to_add:
        attribute_to_add = Attribute(name=name, category=category)
        add_and_commit(attribute_to_add, session)
    return attribute_to_add


def add_bookmark(room, user, session):
    '''
    associate bookmarked room with user in Bookmark table
    if the association doesn't already exist
    '''
    bookmark_to_add = get_row_if_exists(Bookmark, session, **
                                        {'room_id': room.id, 'user_id': user.id})
    if not bookmark_to_add:
        bookmark_to_add = Bookmark(room=room, user=user)
        add_and_commit(bookmark_to_add, session)
    return bookmark_to_add

# Read

def get_row_if_exists(db_obj, session, **condition):
    """
    Check if a row that satisfies a certain condition exists
    :param db_obj: Database Object like User
    :param session: a db connection session
    :param condition: kwargs like dict like {'name':'Cris'}
    :return: the row if a row exists, else None
    """
    row = session.query(db_obj).filter_by(**condition).first()
    return row


def read_rooms(session):
    '''
    return all rooms in the Room table
    '''
    return session.query(Room).all()


def room_json(room, session, test_mode=False):
    '''
    generates a JSON representation of a given room
    in the Room table, also including its attributes
    (House_Attribute), preferred move-in time (Move_In),
    and the user to post the room (User)
    '''
    other_map = {'other': [], 'facilities': []}
    house_attrs = session.query(House_Attribute).filter(
        House_Attribute.room_id == room.id).all()
    house_move_in = session.query(Move_In).filter(
        Move_In.id == room.move_in_id).first()
    house_user = session.query(User).filter(
        User.id == room.user_id).first()
    for ha in house_attrs:
        category_name = session.query(Attribute).filter(
            Attribute.name == ha.attribute_name).first().category
        other_map[category_name].append(ha.attribute_name)
    r_json = room.serialize
    room_name = room.address.serialize['address'].split(",")[0]
    room_photos = ["photo1", "photo2"] if test_mode else \
        get_images("user"
                   + str(house_user.id),
                   extra_path=str(room.id)+"/")
    profile_photo = "profile_photo" if test_mode else HOUSEIT_S3_URL + \
        get_images("user"+str(house_user.id), category="profile")[0]

    return_json = {
        'name': room_name,
        'address': room.address.serialize['address'],
        'distance': room.address.serialize['distance'],
        'pricePerMonth': r_json['price'],
        'from_month': room.stay_period.from_month.strftime("%B/%y"),
        'to_month': room.stay_period.to_month.strftime("%B/%y"),
        'early_date': house_move_in.early_date.strftime("%m/%d/%y"),
        'late_date': house_move_in.late_date.strftime("%m/%d/%y"),
        'roomType': r_json['room_type'],
        'other': other_map['other'],
        'facilities': other_map['facilities'],
        'leaserName': house_user.name,
        'leaserEmail': house_user.email,
        'leaserPhone': house_user.phone,
        'leaserSchoolYear': house_user.school_year,
        'leaserMajor': house_user.major,
        'photos': room_photos,
        'profilePhoto': profile_photo,
        'roomId': r_json['id'],
        'negotiable': r_json['negotiable'],
        'numBaths': r_json['no_bathrooms'],
        'numBeds': r_json['no_rooms'],
        'roomDescription': r_json['description'],
    }
    return return_json


# Update

def update_field(db_obj, session, condition={}, values={}):
    '''
    Updates rows in given db matching condition, using given values.
    condition and values should be dictionaries.
    NOTE: invalid conditions or values WILL throw errors!
    '''
    print("updating the field", condition, values)
    updated_obj = session.query(db_obj).filter_by(**condition).update(values)
    session.commit()
    return updated_obj

# write an attribute to database

def write_attribute(attributes, category, room, session):
    '''
    Posted when user posts a room. 
    Writes list of preferences and facilities of room to the Attribute table.
    Assumes only legal attributes will be added.
    '''
    for attribute in attributes:
        # check if an attribute exists
        new_attribute = get_row_if_exists(
            Attribute, session, **{'name': attribute})
        if not new_attribute:
            new_attribute = add_attribute(attribute, category, session)
        # finally add the house attribute
        add_house_attribute(room, new_attribute, session)

# write a single room to database


def write_room(room_json, session, test_mode=False):
    # TODO: might need to add error handling upon database fail
    # write custom exceptions
    # gets room owner, assuming when a new room gets added the user exists
    room_owner = get_row_if_exists(
        User, session, **{'email': room_json['leaserEmail']})
    room_name = room_json['address'].split(",")[0]
    early_date = datetime.strptime(
        room_json["early_date"], "%m/%d/%y")
    late_date = datetime.strptime(
        room_json["late_date"], "%m/%d/%y")
    new_move_in = get_row_if_exists(Move_In, session, **{
        "early_date": early_date,
        "late_date": late_date
    })
    if not new_move_in:
        new_move_in = add_move_in(early_date,
                                  late_date, session)

    new_address = add_address(room_json['distance'],
                              room_json['address'], session)
    new_stay_period = add_stay_period(
        datetime.strptime(room_json['from_month'], "%B/%y"),
        datetime.strptime(room_json['to_month'], "%B/%y"), session)
    new_room = add_room(datetime.now(),
                        room_json['roomType'],
                        room_json['pricePerMonth'],
                        room_json['negotiable'],
                        room_json['roomDescription'],
                        new_stay_period,
                        new_address,
                        room_owner, new_move_in, int(room_json['numBeds']),
                        float(room_json['numBaths']), session)
    write_attribute(room_json['other'], 'other', new_room, session)
    write_attribute(room_json['facilities'], 'facilities', new_room, session)
    # add photo
    if not test_mode:
        for photo in room_json['photos']:
            path_name = "/".join(["user"+str(room_owner.id), 'housing',
                                  str(new_room.id), photo.filename])
            upload_file_wobject(photo, 'houseit', path_name)  # Change to ID
    return True

# DELETE

def remove_bookmark(room, user, session):
    '''
    de-associates a previously bookmarked room and 
    the user that bookmarked it
    '''
    session.query(Bookmark).filter_by(
        room_id=room.id, user_id=user.id).delete()
    session.commit()
    return

def remove_room(room, session):
    '''
    removes room from db
    '''
    session.query(Room).filter(Room.id == room.id).delete()
    return
