from flask import Flask, render_template, request
from datetime import datetime, timedelta
import mysql.connector
import json
from json import JSONEncoder
from mysql.connector import errorcode

BOOKING_START_DATE_KEY = "start_date"
BOOKING_END_DATE_KEY = "end_date"
BOOKING_NUM_ADULTS_KEY = "num_adults"
BOOKING_NUM_CHILDREN_KEY = "num_kids"
BOOKING_OWNER_NAME_KEY = "owner_name"


class Booking:
    '''
    Class representing a booking. This is the in memory representation off a booking
    '''
    def __init__(self, start_date, end_date, num_adults, num_children, owner_name):
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self.start_date = start_date
        self.end_date = end_date
        self.num_adults = num_adults
        self.num_children = num_children
        self.owner_name = owner_name

    def data(self):
        return self.start_date, self.end_date, self.num_adults, self.num_children, self.owner_name


class DataBaseInteractor:
    '''
    This class intermediates the communication with the database.
    Upon instantiation it uses all the necessary information for a valid connection using the mysql 
    connector.
    The typical interaction would be to open a connection, create a cursor execute the needed query
    and finally close the cursor and the connection
    '''
    def __init__(self):
        self.user: str = "victor@bookingsproject"
        self.password: str = "Felix2010"
        self.host: str = "bookingsproject.mysql.database.azure.com"
        self.db_name: str = "bookings"

    def _open_connection(self):
        '''
        This open a connection to the database
        '''
        try:
            connection = mysql.connector.connect(user=self.user,
                                                 password=self.password,
                                                 host=self.host,
                                                 database=self.db_name)
            return connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            connection.close()
            

    def add(self, booking: Booking, table_name="bookings"):
        '''
        Adds a booking to the database
        '''
        connection = self._open_connection()
        cursor = connection.cursor()

        add_query = (f"INSERT INTO {table_name} "
                     f"({BOOKING_START_DATE_KEY}, {BOOKING_END_DATE_KEY}, {BOOKING_NUM_ADULTS_KEY}, {BOOKING_NUM_CHILDREN_KEY}, {BOOKING_OWNER_NAME_KEY}) "
                     f"VALUES "
                     f"(%s, %s, %s, %s, %s)")

        cursor.execute(add_query, booking.data())
        connection.commit()
        cursor.close()
        connection.close()

    def get_bookings(self, table_name="bookings"):
        '''
        returns the contents of a table from the database in json format
        '''
        connection = self._open_connection()
        cursor = connection.cursor()
        cursor.execute(f'SELECT*FROM {table_name}')
        data = cursor.fetchall()
        results = []
        for row in data:
            result = {}
            result[BOOKING_START_DATE_KEY]=row[1]
            if row[1]:
                result[BOOKING_START_DATE_KEY]=row[1].strftime("%b %d %Y")
            result[BOOKING_END_DATE_KEY]=row[2]
            if row[2]:
                result[BOOKING_END_DATE_KEY]=row[2].strftime("%b %d %Y")
            result[BOOKING_NUM_ADULTS_KEY]=row[3]
            result[BOOKING_NUM_CHILDREN_KEY]=row[4]
            result[BOOKING_OWNER_NAME_KEY]=row[5]
            results.append(result)
        print(results)
        cursor.close()
        connection.close()
        return app.response_class(response=json.dumps(results),status=200, mimetype='application/json')


def add_to_db(start_date, end_date, num_adults, num_children, name): 
    db_interactor = DataBaseInteractor()
    new_entry = Booking(
        start_date=start_date,
        end_date=end_date,
        num_adults=num_adults,
        num_children=num_children,
        owner_name=name)
    db_interactor.add(new_entry)


app = Flask(__name__, template_folder='./frontend', static_folder='./frontend/static')

@app.route('/') #Entry point of the website
def entry_point_site():
    return render_template('index.html')

@app.route('/<home_index>') # entry point to lead to index.html 
def entry_point_site_with_file(home_index):
    return render_template(f'{home_index}')

@app.route('/about/<about_index>') # entry point for about page
def about(about_index):
    return render_template(f'about/{about_index}')

@app.route('/gallery/<gallery_index>') # entry point for gallery
def galery(gallery_index):
    return render_template(f'gallery/{gallery_index}')

@app.route('/contact/<contact_index>') # entry point for contact page
def contact(contact_index):
    return render_template(f'contact/{contact_index}')

@app.route('/see&do/<see_index>') # entry point for  see&do page
def see_do(see_index):
    return render_template(f'see&do/{see_index}')

@app.route('/login/<login_index>') # entry point for login page
def login(login_index):
    return render_template(f'login/{login_index}')

@app.route('/add') 
def add():
    start_date = request.args.get(BOOKING_START_DATE_KEY)
    end_date = request.args.get(BOOKING_END_DATE_KEY)
    num_adults = request.args.get(BOOKING_NUM_ADULTS_KEY)
    num_children = request.args.get(BOOKING_NUM_CHILDREN_KEY)
    owner_name = request.args.get(BOOKING_OWNER_NAME_KEY)
    add_to_db(start_date, end_date, num_adults, num_children, owner_name)
    return render_template('index.html')

@app.route('/get_bookings')
def get_bookings():
    db_interactor = DataBaseInteractor()
    return db_interactor.get_bookings()
    


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='80')
