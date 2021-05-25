from flask import Flask, render_template, request
from datetime import datetime, timedelta


import mysql.connector
from mysql.connector import errorcode

BOOKING_START_DATE_KEY = "start_date"
BOOKING_END_DATE_KEY = "end_date"
BOOKING_NUM_ADULTS_KEY = "num_adults"
BOOKING_NUM_CHILDREN_KEY = "num_kids"
BOOKING_OWNER_NAME_KEY = "owner_name"

class Booking:
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
    def __init__(self):
        self.user: str = "victor@bookingsproject"
        self.password: str = "Felix2010"
        self.host: str = "bookingsproject.mysql.database.azure.com"
        self.db_name: str = "bookings"

    def _open_connection(self):
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

@app.route('/')
def entry_point_site():
    return render_template('index.html')

@app.route('/<home_index>')
def entry_point_site_with_file(home_index):
    return render_template(f'{home_index}')

@app.route('/about/<about_index>')
def about(about_index):
    return render_template(f'about/{about_index}')

@app.route('/gallery/<gallery_index>')
def galery(gallery_index):
    return render_template(f'gallery/{gallery_index}')

@app.route('/contact/<contact_index>')
def contact(contact_index):
    return render_template(f'contact/{contact_index}')

@app.route('/see&do/<see_index>')
def see_do(see_index):
    return render_template(f'see&do/{see_index}')

@app.route('/add')
def add():
    start_date = request.args.get(BOOKING_START_DATE_KEY)
    end_date = request.args.get(BOOKING_END_DATE_KEY)
    num_adults = request.args.get(BOOKING_NUM_ADULTS_KEY)
    num_children = request.args.get(BOOKING_NUM_CHILDREN_KEY)
    owner_name = request.args.get(BOOKING_OWNER_NAME_KEY)
    add_to_db(start_date, end_date, num_adults, num_children, owner_name)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
