from attr import attrs, attrib
import operator
from datetime import datetime

@attrs
class Filter(object):
    input_json = attrib()

    def verify_price_range(self, price_range: list) -> bool:
        # asserting that the input is a list of 2 items
        if((type(price_range)!=list) or (len(price_range)!=2)):
            return False
        min_price = price_range[0]
        max_price = price_range[1]
        # asserting that both price inputs are integers
        if((type(min_price)!=int) or (type(max_price)!=int)):
            return False
        # asserting that both prices are positive and min price is less than max
        if((min_price>max_price) or (min_price<0) or (max_price<0)):
            return False

        return True

    def verify_room_type(self, room_type: dict) -> bool:
        # asserting input is a dictionary with 2 key,value pairs
        if((type(room_type)!=dict) or (len(room_type)!=2)):
            return False
        # asserting that all values of dictionary are tuples
        for value in room_type.values():
            if type(value)!=tuple:
                return False
        
        bed_count = room_type["Bedrooms"][0]
        bath_count = room_type["Bathrooms"][0]
        bed_operator = room_type["Bedrooms"][1]
        bath_operator = room_type["Bathrooms"][1]
        valid_operators = [operator.eq, operator.le]

        # asserting that inputs can either be a number or a number+ 
        if((bed_operator not in valid_operators) or (bath_operator not in valid_operators)):
            return False
        # asserting that all bedroom counts are positive ints 
        if((type(bed_count)!=int) or (bed_count<0)):
            return False
        # asserting that all bathroom counts are positive floats 
        if((type(bath_count)!=float) or (bath_count<0)):
            return False

        return True

    def verify_distance(self, distance: tuple) -> bool:
        # asserting that input is given as tuple of distance and operator
        if((type(distance)!=tuple) or (type(distance[0])!=str) or (len(distance[0])<3)):
            return False
        else:
            time_per = distance[0][:2]
            distance_op = distance[1]
            # asserting that distance is given as numbers and operators are either >= or <=
            if((not time_per.isdigit()) or (distance_op!=operator.le) or (distance_op!=operator.ge)):
                return False

        return True

    def verify_availability(self, availability: dict) -> bool:
        # asserting input is a dictionary with 2 key,value pairs
        if((type(availability)!=dict) or (len(availability)!=2)):
            return False
        # asserting that all values of dictionary are strings
        for value in availability.values():
            if type(value)!=str:
                return False
        month = availability["Month"]
        year = availability["Year"]
        valid_months = ["january", "february", "march", "april", "may", "june", "july",
         "august", "september", "october", "november", "december"]

        # assert month and year are valid inputs 
        if((month.lower() not in valid_months)):
            return False
        if((len(year)!=4) or (not year.isdigit())):
            return False
        return True

    
