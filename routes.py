from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from src.BookingError import BookingError
from server import app, system, auth_manager
from datetime import datetime
from src.Location import Location
from src.client import bootstrap_system


@app.route('/')
def home():
    
    return render_template('home.html');

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Task 1: complete this function
    """
    if request.method == 'POST':
        user_id = request.form["username"]
        password = request.form["password"]
        
        if system.login_customer(user_id, password):
            return redirect(url_for('home'))
        else:
            return "Incorrect username or password"
   #     user_obj = auth_manager.login(user_id, password) 
    #    if user_obj == None:
     #      return "Incorrect username or password"
      #  else: 
       #    return redirect(url_for('home'))
        
        # Next helps with redirecting the user to the previous page
        
        redir = request.args.get('next')
        return redirect(redir or url_for('home'))
    
    return render_template('login.html')



@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():

    '''
    TASK 4.1 complete this function
    '''
    if request.method == 'POST':
        user = request.form['admin_username']
        password = request.form['admin_password']
        
        if system.login_admin(user, password): 
            return redirect(url_for('home'))
        else:
            return "Incorrect username or password"
            
        redir = request.args.get('next')
        return redirect(redir or url_for('home'))

    return render_template('login.html', )

@app.route('/logout')
@login_required
def logout():
    auth_manager.logout()
    return redirect(url_for('home'))



'''
    Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404



'''
    Search for Cars
'''
@app.route('/cars', methods =["GET", "POST"])
@login_required
def cars():
    """
    Task 2: At the moment this endpoint does not do anything if a search
    is sent. It should filter the cars depending on the search criteria
    """
    cars = system.cars    
    if request.method == 'POST':
        make = request.form["make"]
        model = request.form["model"]       
        cars = system.car_search(make, model)
    return render_template('cars.html', cars = cars)



'''
    Display car details for the car with given rego
'''

@app.route('/cars/<rego>', methods = ["GET", "POST"])
@login_required
def car(rego):
    car = system.get_car(rego)
    #rating = 5
    if not car:
        abort(404)
    

    #ratings_list = system.add_rating(rating)
    #new_rating = sum(ratings_list)/len(ratings_list)
    #rating = new_rating

    return render_template('car_details.html', car=car)



'''
    Make a booking for a car with given rego
'''
@app.route('/cars/book/<rego>', methods=["GET", "POST"])
@auth_manager.customer_required
def book(rego):
    car = system.get_car(rego)

    if not car:
        abort(404)
    
    if request.method == 'POST':
        date_format = "%Y-%m-%d"
        
  
        s_date = request.form['start_date']
        e_date = request.form['end_date']
        if s_date == '':
            return render_template('booking_form.html', error = 'Specify a valid start date')
        elif e_date == '':
            return render_template('booking_form.html', error = 'Specify a valid end date')
           
        start_date  = datetime.strptime(request.form['start_date'], date_format)
        end_date    = datetime.strptime(request.form['end_date'],   date_format)
        start_loc = request.form['start']
        end_loc = request.form['end']
        
        num_days = (end_date - start_date).days + 1

        if 'check' in request.form:
            fee = car.get_fee(num_days)
            
            return render_template(
                'booking_form.html',
                confirmation=True,
                form=request.form,
                car=car,
                fee=fee
            ) 

        elif 'confirm' in request.form:
            location = Location(request.form['start'], request.form['end'])    
                   
            try:    
                booking  = system.make_booking(current_user, num_days, car, location, start_date, end_date, start_loc, end_loc)
            except BookingError as error:                 
                return render_template('booking_form.html', error = error.message)
            else:
                return render_template('booking_confirm.html', booking = booking)
            
    return render_template('booking_form.html', car=car)


'''
    Display list of all bookings for the car with given 'rego'
'''
@app.route('/cars/bookings/<rego>')
@login_required
def car_bookings(rego):
    """
    Task 3: This should render a new template that shows a list of all
    the bookings associated with the car represented by 'rego'
    """
    
    car = system.get_car(rego)
    bookings = car.bookings
    
    '''
    list = []    
    for booking in bookings:
            list.append(booking) 
    return list
    '''
    print(bookings) 
    
    return render_template('bookings.html', bookings = bookings)


'''
    View all current bookings
'''
@app.route('/cars/bookings')
@auth_manager.admin_required

def all_bookings():

    '''
    Task 4.2: This should render a list of all current bookings
    on the system
    '''
    
    bookings = system.bookings
    #print(bookings)
    '''
    list = []    
    for booking in bookings:
            list.append(booking) 
    return list
    
    '''
    
  #  return '<h1> Needs to be implemented </h1>'
    return render_template('bookings.html')

'''
    Add a new car to the system
'''
from src.CarFactory import CarFactory
@app.route('/add_car', methods=['GET', 'POST'])
@auth_manager.admin_required
def add_car():
    
    car_factory = CarFactory()
    
    if request.method == 'POST':
        
        name = request.form['name']
        model = request.form['model']
        rego = request.form['rego']
        car_type = request.form['car-type']
        
        car = car_factory.make_car(name, model, rego, car_type)
        system.add_car(car)
     
        
    '''
    Task 4.3: This should allow the admin to register
    new cars to the system, using the method provided
    in the CarFactory class.
    
    Provide meaningful message upon success
    '''

    return render_template('car_register_form.html')
    
    
