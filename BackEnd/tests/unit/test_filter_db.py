import unittest
import os
import app.filter.filter_db

TEST_DB_NAME = "housing_test.db"
TEST_DB_STRING = "sqlite:///housing_test.db"

class TestFilterDb(unittest.TestCase):
    def setUp(self):
        createDB(TEST_DB_STRING)
        self.session = crud.getSession(TEST_DB_STRING)

    def tearDown(self):
        os.remove(TEST_DB_NAME)

    def test_one_criteria(self):
        return

    def test_multiple_criteria(self):
        return

    def test_invalid_price_range(self):
        return

    def test_invalid_price_type(self):
        return
    
    def test_invalid_date(self):
        return

    def test_invalid_availability(self):
        return

    def test_invalid_distance(self):
        return

    def test_no_result(self):
        return
    
    def test_room_type(self):
        return
    
    
