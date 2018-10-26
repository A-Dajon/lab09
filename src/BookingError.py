
class BookingError(Exception):
    
    def __init__(self, message, field_name):
        
        self._field_name = field_name
        self._message = message        
    
    
    @property
    def field_name(self):
        return self._field_name

    @property
    def message(self):
        return self._message

