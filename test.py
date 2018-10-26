from src.client import bootstrap_system
from src.AuthenticationManager import AuthenticationManager
import unittest
import pytest
from src.Location import Location
from datetime import datetime

class DummyAuthenticationManager(AuthenticationManager):
    def __init__(self):
        super().__init__(None)

    def login(self, user, username, password):
        if user.username == username and user.validate_password(password):
            return user
        return None

class TestMakeBooking(unittest.TestCase):

    def setUp(self):
        self.system = bootstrap_system(DummyAuthenticationManager())

    def test_successful_make_booking(self):
        print("test_successful_make_booking")
        date_format = "%Y-%m-%d"
        date = datetime.strptime('2018-10-20', date_format).date()
        start_loc = "Start"
        end_loc = "End"
        start_date = "2018-5-20"
        end_date = "2018-5-23"
        location = Location(start_loc, end_loc)
        
        original_booking_size = len(self.system._bookings)
        
        car = self.system.cars[0]
        customer = self.system.login_customer('Matt', 'pass')
        self.system.make_booking(customer, 3 , car, location, start_date, end_date, start_loc, end_loc)     
        assert len(self.system._bookings) == original_booking_size + 1
        assert self.system._bookings[original_booking_size].location.pickup == start_loc
        assert self.system._bookings[original_booking_size].location.dropoff == end_loc
        assert self.system._bookings[original_booking_size].booking_fee == 150


    def test_unsuccessful_booking_no_start_location_specified(self):
        with pytest.raises(Exception) as error:           
            date_format = "%Y-%m-%d"
            date = datetime.strptime('2018-10-20', date_format).date()
            start_loc = ""
            end_loc = "End"
            start_date = "2018-5-20"
            end_date = "2018-5-23"
            location = Location(start_loc, end_loc)
            num_days = (end_date - start_date).days + 1
            
            car = self.system.cars[0]
            customer = self.system.login_customer('Matt', 'pass')
              
            original_booking_size = len(self.system._bookings)
            self.system.make_booking(customer, num_days , car, location, start_date, end_date, start_loc, end_loc) 
            
    def test_unsuccessful_booking_no_start_location_specified(self):
        with pytest.raises(Exception) as error:           
            date_format = "%Y-%m-%d"
            date = datetime.strptime('2018-10-20', date_format).date()
            start_loc = "Start"
            end_loc = ""
            start_date = "2018-5-20"
            end_date = "2018-5-23"
            location = Location(start_loc, end_loc)
            num_days = (end_date - start_date).days + 1
            
            car = self.system.cars[0]
            customer = self.system.login_customer('Matt', 'pass')
              
            original_booking_size = len(self.system._bookings)
            self.system.make_booking(customer, num_days , car, location, start_date, end_date, start_loc, end_loc) 

    def test_unsuccessful_booking_no_start_date_specified(self):
        with pytest.raises(Exception) as error:           
            date_format = "%Y-%m-%d"
            date = datetime.strptime('2018-10-20', date_format).date()
            start_loc = "Start"
            end_loc = "End"
            start_date = ""
            end_date = "2018-5-23"
            location = Location(start_loc, end_loc)
            num_days = (end_date - start_date).days + 1
            
            car = self.system.cars[0]
            customer = self.system.login_customer('Matt', 'pass')
              
            original_booking_size = len(self.system._bookings)
            self.system.make_booking(customer, num_days , car, location, start_date, end_date, start_loc, end_loc) 
            
    def test_unsuccessful_booking_no_end_date_specified(self):
        with pytest.raises(Exception) as error:           
            date_format = "%Y-%m-%d"
            date = datetime.strptime('2018-10-20', date_format).date()
            start_loc = "Start"
            end_loc = "End"
            start_date = "2018-5-23"
            end_date = ""
            location = Location(start_loc, end_loc)
            num_days = (end_date - start_date).days + 1
            
            car = self.system.cars[0]
            customer = self.system.login_customer('Matt', 'pass')
              
            original_booking_size = len(self.system._bookings)
            self.system.make_booking(customer, num_days , car, location, start_date, end_date, start_loc, end_loc)
            
            
    def test_unsuccessful_booking_no_end_date_specified(self):
        with pytest.raises(Exception) as error:           
            date_format = "%Y-%m-%d"
            date = datetime.strptime('2018-10-20', date_format).date()
            start_loc = "Start"
            end_loc = "End"
            start_date = "2018-5-23"
            end_date = "2017-01-01"
            location = Location(start_loc, end_loc)
            num_days = (end_date - start_date).days + 1
            
            car = self.system.cars[0]
            customer = self.system.login_customer('Matt', 'pass')
              
            original_booking_size = len(self.system._bookings)
            self.system.make_booking(customer, num_days , car, location, start_date, end_date, start_loc, end_loc) 


        
