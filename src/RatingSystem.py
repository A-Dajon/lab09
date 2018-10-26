class RatingSystem():

    def __init__(self):
    #    self._car = car
        self._ratings = []

    def add_car_rating(self, rating):
 
        self._ratings.append(rating)

    def calculate_average(self, ratings):
        if len(ratings) == 0:
            return ratings
        else:
            average = sum(ratings)/len(ratings)
            return average

    @property
    def ratings(self):
        return self._ratings
        
