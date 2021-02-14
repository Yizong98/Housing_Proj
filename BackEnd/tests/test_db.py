import unittest
import app.db.crud as crud
from datetime import datetime
from app.db.database_setup import *
from app.assets.options import others, room_types, facilities
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import os

TEST_DB_NAME = 'housing_test.db'
TEST_DB_STRING = 'sqlite:///housing_test.db'


class TestDbOperations(unittest.TestCase):
    def setUp(self):
        createDB(TEST_DB_STRING)
        self.session = crud.getSession(TEST_DB_STRING)

    def tearDown(self):
        os.remove(TEST_DB_NAME)

    def test_createdb(self):
        # check if the db is generated
        is_exist = os.path.exists(TEST_DB_NAME)
        self.assertEqual(is_exist, True)

    def test_add_user(self):
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"

        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # check if the return object has correct information
        self.assertEqual(user_object.email, user_email)
        self.assertEqual(user_object.name, user_name)
        self.assertEqual(user_object.date_created, created_time)
        self.assertEqual(user_object.phone, user_phone)
        self.assertEqual(user_object.description, user_description)
        self.assertEqual(user_object.school_year, user_school_year)
        self.assertEqual(user_object.major, user_major)

        # check if the user is loaded into the database
        query_object = crud.get_row_if_exists(
            User,
            self.session,
            **{'email': user_email})

        self.assertEqual(query_object == user_object, True)

    def test_add_stay_period(self):
        from_month = datetime(2018, 6, 1)
        to_month = datetime(2018, 7, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # check if the return object has correct information
        self.assertEqual(stay_period_object.from_month, from_month)
        self.assertEqual(stay_period_object.to_month, to_month)

        # check if the stay period is loaded into the database
        query_object = crud.get_row_if_exists(
            Stay_Period,
            self.session,
            **{'from_month': from_month, 'to_month': to_month})

        self.assertEqual(query_object == stay_period_object, True)

        # one thing in the database
        number_of_rows = self.session.query(Stay_Period).count()
        self.assertEqual(number_of_rows == 1, True)

    def test_add_address(self):
        address = "75 Big Rock Cove St.Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # check if the return object has correct information
        self.assertEqual(address_object.distance, distance)
        self.assertEqual(address_object.address, address)

        # check if the address is loaded into the database
        query_object = crud.get_row_if_exists(
            Address,
            self.session,
            **{'distance': distance, 'address': address})

        self.assertEqual(query_object == address_object, True)

        # one thing in the database
        number_of_rows = self.session.query(Address).count()
        self.assertEqual(number_of_rows == 1, True)

    def test_add_attribute(self):
        name, category = others[0], "other"
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        # check if the return object has correct information
        self.assertEqual(attribute_object.name, name)
        self.assertEqual(attribute_object.category, category)

        # check if the attribute is loaded into the database
        query_object = crud.get_row_if_exists(
            Attribute,
            self.session,
            **{'name': name, 'category': category})

        self.assertEqual(query_object == attribute_object, True)

        # one thing in the database
        number_of_rows = self.session.query(Attribute).count()
        self.assertEqual(number_of_rows == 1, True)

        # check duplicate handling
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        number_of_rows = self.session.query(Attribute).count()
        self.assertEqual(number_of_rows == 1, True)

    def test_add_house_attribute(self):
        name, category = others[0], "other"

        # create an attribute (Single Case)
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        # create a stay period
        from_month = datetime(2018, 6, 1)
        to_month = datetime(2018, 7, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # create an address
        address = "75 Big Rock Cove St.Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # create a move in
        early_date = datetime(2018, 6, 1)
        late_date = datetime(2018, 6, 12)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # create a room
        date_created = datetime.now()
        room_type = room_types[0]
        price = 500
        negotiable = True
        description = "dream house in a life time"
        no_rooms = 2
        no_bathrooms = 2
        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        # connect room with the attribute
        house_attribute_object = crud.add_house_attribute(
            room_object,
            attribute_object,
            self.session)

        # check if the return object has correct information
        self.assertEqual(house_attribute_object.room_id, room_object.id)
        self.assertEqual(house_attribute_object.attribute_name,
                         attribute_object.name)

        # one thing in the database
        number_of_rows = self.session.query(House_Attribute).count()
        self.assertEqual(number_of_rows == 1, True)

        # create two attributes (multiple Case)
        name, category = others[1], "other"

        # create a second attribute
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        house_attribute_object = crud.add_house_attribute(
            room_object,
            attribute_object,
            self.session)

        # check if the return object has correct information
        self.assertEqual(house_attribute_object.room_id, room_object.id)
        self.assertEqual(house_attribute_object.attribute_name,
                         attribute_object.name)

        # two things in the database
        number_of_rows = self.session.query(House_Attribute).count()
        self.assertEqual(number_of_rows == 2, True)

        # check duplicate handling
        house_attribute_object = crud.add_house_attribute(
            room_object,
            attribute_object,
            self.session)

        number_of_rows = self.session.query(House_Attribute).count()
        self.assertEqual(number_of_rows == 2, True)

    def test_add_and_remove_bookmark(self):
        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # create a move in
        early_date = datetime(2018, 6, 1)
        late_date = datetime(2018, 6, 12)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # create a stay period
        from_month = datetime(2018, 6, 1)
        to_month = datetime(2018, 7, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # create an address
        address = "75 Big Rock Cove St. Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # create a room
        date_created = datetime.now()
        room_type = room_types[0]
        price = 500
        negotiable = True
        description = "dream house in a life time"
        no_rooms = 2
        no_bathrooms = 2
        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        # connect bookmark with the room and user
        bookmark_object = crud.add_bookmark(
            room_object,
            user_object,
            self.session)

        # check if the return object has correct information
        self.assertEqual(bookmark_object.room_id, room_object.id)
        self.assertEqual(bookmark_object.user_id, user_object.id)

        # check duplicate handling
        bookmark_object = crud.add_bookmark(
            room_object,
            user_object,
            self.session)

        number_of_rows = self.session.query(Bookmark).count()
        self.assertEqual(number_of_rows == 1, True)

        # check delete
        crud.remove_bookmark(
            room_object,
            user_object,
            self.session)

        number_of_rows = self.session.query(Bookmark).count()
        self.assertEqual(number_of_rows == 0, True)

        crud.remove_bookmark(
            room_object,
            user_object,
            self.session)

        number_of_rows = self.session.query(Bookmark).count()
        self.assertEqual(number_of_rows == 0, True)

    def test_get_row_if_exists(self):
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"

        # check if it the method detects no users
        query_object = crud.get_row_if_exists(
            User,
            self.session,
            **{'email': user_email})

        self.assertEqual(query_object is None, True)

        # add the user
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # check if it the method detects an user
        query_object = crud.get_row_if_exists(
            User,
            self.session,
            **{'email': user_email})

        self.assertEqual(query_object == user_object, True)

    def test_read_rooms(self):
        # add room allows duplicates since one can have multiple rooms same time with same criteria
        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # create a move in
        early_date = datetime(2018, 6, 1)
        late_date = datetime(2018, 6, 12)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # create a stay period
        from_month = datetime(2018, 6, 1)
        to_month = datetime(2018, 7, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # create an address
        address = "75 Big Rock Cove St.Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # create a room
        date_created = datetime.now()
        room_type = room_types[0]
        price = 500
        negotiable = True
        description = "dream house in a life time"
        no_rooms = 2
        no_bathrooms = 2
        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        number_of_rows = len(crud.read_rooms(self.session))
        self.assertEqual(number_of_rows == 3, True)

        # create a different user
        user_name = "keenan"
        user_email = "keenan@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-8888"
        user_description = "HK Dutch man"
        user_school_year = "Grad"
        user_major = "Computer Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # create a move in
        early_date = datetime(2018, 8, 1)
        late_date = datetime(2018, 10, 12)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # create a stay period
        from_month = datetime(2018, 10, 1)
        to_month = datetime(2019, 10, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # create an address
        address = "75 Big Rock Cove St.Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # create a room
        date_created = datetime.now()
        room_type = room_types[0]
        price = 500
        negotiable = True
        description = "smoking is bad for your health"
        no_rooms = 4
        no_bathrooms = 5
        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        number_of_rows = len(crud.read_rooms(self.session))
        self.assertEqual(number_of_rows == 4, True)

    def test_room_json(self):
        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # create a move in
        early_date = datetime(2018, 6, 1)
        late_date = datetime(2018, 6, 12)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # create a stay period
        from_month = datetime(2018, 6, 1)
        to_month = datetime(2018, 7, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # create an address
        address = "75 Big Rock Cove St.Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # create a room
        date_created = datetime.now()
        room_type = room_types[0]
        price = 500
        negotiable = True
        description = "dream house in a life time"
        no_rooms = 2
        no_bathrooms = 2
        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        result_json = crud.room_json(
            room_object,
            self.session,
            True)

        self.assertEqual(result_json["name"] ==
                         "75 Big Rock Cove St.Middletown", True)
        self.assertEqual(result_json["address"] == address, True)
        self.assertEqual(result_json["pricePerMonth"] == price, True)
        self.assertEqual(result_json["from_month"] == "June/18", True)
        self.assertEqual(result_json["to_month"] == "July/18", True)
        self.assertEqual(result_json["early_date"] == "06/01/18", True)
        self.assertEqual(result_json["late_date"] == "06/12/18", True)
        self.assertEqual(result_json["roomType"] == room_type, True)
        self.assertEqual(result_json["other"] == [], True)
        self.assertEqual(result_json["facilities"] == [], True)
        self.assertEqual(result_json["leaserName"] == user_name, True)
        self.assertEqual(result_json["leaserEmail"] == user_email, True)
        self.assertEqual(result_json["leaserPhone"] == user_phone, True)
        self.assertEqual(
            result_json["leaserSchoolYear"] == user_school_year, True)
        self.assertEqual(result_json["leaserMajor"] == user_major, True)
        self.assertEqual(result_json["photos"] == ["photo1", "photo2"], True)
        self.assertEqual(result_json["profilePhoto"] == "profile_photo", True)
        self.assertEqual(result_json["roomId"] == room_object.id, True)
        self.assertEqual(result_json["negotiable"] == negotiable, True)
        self.assertEqual(result_json["numBaths"] == no_rooms, True)
        self.assertEqual(result_json["numBeds"] == no_bathrooms, True)
        self.assertEqual(result_json["roomDescription"] == description, True)

        # add three attributes
        name, category = others[0], "other"

        # create an attribute
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        # connect room with the attribute
        house_attribute_object = crud.add_house_attribute(
            room_object,
            attribute_object,
            self.session)

        name, category = others[1], "other"

        # create an attribute
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        # connect room with the attribute
        house_attribute_object = crud.add_house_attribute(
            room_object,
            attribute_object,
            self.session)

        name, category = facilities[0], "facilities"

        # create an attribute
        attribute_object = crud.add_attribute(
            name,
            category,
            self.session)

        # connect room with the attribute
        house_attribute_object = crud.add_house_attribute(
            room_object,
            attribute_object,
            self.session)

        result_json = crud.room_json(
            room_object,
            self.session,
            True)

        self.assertEqual(result_json["other"] == [others[0], others[1]], True)
        self.assertEqual(result_json["facilities"] == [facilities[0]], True)

    def test_add_move_in(self):
        early_date = datetime(2018, 6, 1)
        late_date = datetime(2018, 8, 1)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # check if return object has correct info
        self.assertEqual(move_in_object.early_date, early_date)
        self.assertEqual(move_in_object.late_date, late_date)

        # check if move in is loaded in db
        query_object = crud.get_row_if_exists(
            Move_In,
            self.session,
            **{'early_date': early_date, 'late_date': late_date})

        self.assertEqual(query_object == move_in_object, True)

        # check that there's only one thing in db
        number_of_rows = self.session.query(Move_In).count()
        self.assertEqual(number_of_rows == 1, True)

    def test_write_room(self):
        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # the input json should be the same as output json from room_json except for id
        test_json = {'name': '75 Big Rock Cove St. Middletown',
                     'address': '75 Big Rock Cove St. Middletown, NY 10940',
                     'distance': '20 mins', 'pricePerMonth': 500,
                     'from_month': 'June/18', 'to_month': 'July/18',
                     'early_date': '06/01/18', 'late_date': '06/12/18',
                     'roomType': 'Single', 'other': [], 'facilities': [],
                     'leaserName': 'cris', 'leaserEmail': 'haha@ucsd.edu',
                     'leaserPhone': '858-2867-3567',
                     'leaserSchoolYear': 'Third',
                     'leaserMajor': 'Data Science',
                     'photos': ['photo1', 'photo2'],
                     'profilePhoto': 'profile_photo',
                     'negotiable': True,
                     'numBaths': 2.5,
                     'numBeds': 2,
                     'roomDescription': 'dream house in a life time'}

        crud.write_room(test_json, self.session, True)

        room_object = crud.get_row_if_exists(
            Room,
            self.session,
            **{'id': 1})

        self.assertEqual(room_object is not None, True)

        result_json = crud.room_json(
            room_object,
            self.session,
            True)

        test_json['roomId'] = 1

        self.assertEqual(result_json == test_json, True)

    def test_write_attribute(self):
        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # create a move in
        early_date = datetime(2018, 6, 1)
        late_date = datetime(2018, 6, 12)
        move_in_object = crud.add_move_in(
            early_date,
            late_date,
            self.session)

        # create a stay period
        from_month = datetime(2018, 6, 1)
        to_month = datetime(2018, 7, 1)
        stay_period_object = crud.add_stay_period(
            from_month,
            to_month,
            self.session)

        # create an address
        address = "75 Big Rock Cove St.Middletown, NY 10940"
        distance = "20 mins"
        address_object = crud.add_address(
            distance,
            address,
            self.session)

        # create a room
        date_created = datetime.now()
        room_type = room_types[0]
        price = 500
        negotiable = True
        description = "dream house in a life time"
        no_rooms = 2
        no_bathrooms = 2
        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        room_object = crud.add_room(
            date_created,
            room_type,
            price,
            negotiable,
            description,
            stay_period_object,
            address_object,
            user_object,
            move_in_object,
            no_rooms,
            no_bathrooms,
            self.session)

        crud.write_attribute(
            facilities[0:3],
            'facilities',
            room_object,
            self.session)

        count = self.session.query(House_Attribute).count()
        self.assertEqual(count == 3, True)

        categories = self.session.query(Attribute.category).distinct().all()
        self.assertEqual(categories[0][0] == 'facilities', True)

        names = set([result[0]
                     for result in self.session.query(Attribute.name).all()])
        self.assertEqual(names == set(facilities[0:3]), True)

    def test_update_field(self):
        # create an user
        user_name = "cris"
        user_email = "haha@ucsd.edu"
        created_time = datetime.now()
        user_phone = "858-2867-3567"
        user_description = "cultured man"
        user_school_year = "Third"
        user_major = "Data Science"
        user_object = crud.add_user(
            user_name,
            user_email,
            created_time,
            user_phone,
            user_description,
            user_school_year,
            user_major,
            self.session)

        # change description
        crud.update_field(
            User,
            self.session,
            {'email': 'haha@ucsd.edu'},
            {'description': 'google man'})

        user_object = crud.get_row_if_exists(
            User,
            self.session,
            **{'email': 'haha@ucsd.edu'})

        self.assertEqual(user_object.description == 'google man', True)


if __name__ == '__main__':
    unittest.main()
