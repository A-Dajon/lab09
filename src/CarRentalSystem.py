from src.Booking import Booking
from src.BookingError import BookingError
import copy


class CarRentalSystem:
    def __init__(self, admin_system, auth_manager):
        self._cars = []
        self._customers = []
        self._bookings = []
        self._admin_system = admin_system
        self._auth_manager = auth_manager


    '''
    Query Processing Services
    '''
    def car_search(self, name=None, model=None):
    
        matches = []        
        for car in self._cars:
            if (car.name.lower() == name.lower() or car.model.lower() == model.lower()):
                matches.append(car)
        if len(matches) == 0:
                return self._cars
        
        return matches


    def get_user_by_id(self, user_id):
        for c in self._customers:
            if c.get_id() == user_id:
                return c

        return self._admin_system.get_user_by_id(user_id)
            

    def get_car(self, rego):
        for c in self.cars:
            if c.rego == rego:
                return c
        return None
    


    '''
    Booking Services
    '''
    def make_booking(self, customer, period, car, location, s_date, e_date, s_loc, e_loc):
        # Prevent the customer from referencing 'current_user';
        # otherwise the customer recorded in each booking will be modified to
        # a different user whenever the current_user changes (i.e. when new user logs-in)
        

        if s_loc == "":
          booking_error = BookingError("Specify a valid start location", s_loc)
          raise booking_error
        elif e_loc == "":
          booking_error = BookingError("Specify a valid end location", e_loc)
          raise booking_error
        elif s_date == "":
          booking_error = BookingError("Specify a valid start date", s_date)
          raise booking_error
        elif e_date == "":
          booking_error = BookingError("Specify a valid end date", e_date)
          raise booking_error
        # Check that end date is not before start date
        elif period < 0:
          booking_error = BookingError("Specify a valid booking period", period)
          raise booking_error
        else:   
          new_booking = Booking(customer, period, car, location)
          self._bookings.append(new_booking)
          car.add_booking(new_booking)
          return new_booking

 #   Registration Services
    

    def add_car(self, car):
        self._cars.append(car)


    def add_customer(self, customer):
        self._customers.append(customer)



    '''
    Login Services
    '''

    def login_customer(self, username, password):
        for customer in self._customers:
            if self._auth_manager.login(customer, username, password):
                return True
        return False

    def login_admin(self, username, password):
        return self._admin_system.login(username, password)



    '''
    Properties
    '''
    @property
    def cars(self):
        return self._cars


    @property
    def bookings(self):
        return self._bookings
