import requests
import mysql.connector

try:
    db = mysql.connector.connect(
        host='localhost',
        user="root",
        password="root",
        auth_plugin='mysql_native_password',
        database="store_database"
    )
except:
    print('could not connect to database')
    exit()

mycursor = db.cursor()

mycursor.execute('''create table store_info (
    Id int primary key,
    Store_Name varchar(50), 
    Phone varchar(20),
    street varchar(50),
    suburb varchar(50), 
    state varchar(10), 
    postcode int,
    Latitude float(10),
    Longitude float(10), 
    Store_URL varchar(100),
    opening_hours_current_week text,
    opening_hours_next_week text
)''')

def generate_hiffened_name(name):
    hiffened_name = ''

    for char in name:
        if char.isspace():
            hiffened_name = hiffened_name + '-'
        else:
            hiffened_name = hiffened_name + char

    return f'https://www.bigw.com.au/store/{id}/{hiffened_name}'


try:
    response = requests.get('https://api.bigw.com.au/api/stores/v0/list')
    data = response.json()
except:
    print('could not fetch data')
    exit()


for key in data:
    id = data[key]['id']
    name = data[key]['name']
    phone = data[key]['phoneNumber']
    street = data[key]['address']['street']
    suburb = data[key]['address']['suburb']
    state = data[key]['address']['state']
    postcode = data[key]['address']['postcode']
    latitude = data[key]['location']['lat']
    longitude = data[key]['location']['lng']
    store_url = generate_hiffened_name(name)

    this_week = data[key]['tradingHours'][0]['hours']
    next_week = data[key]['tradingHours'][1]['hours']

    mycursor.execute('''INSERT INTO store_info 
    (Id,Store_Name,Phone,street,suburb,state,postcode,Latitude,Longitude,Store_URL,opening_hours_current_week,opening_hours_next_week) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', 
    (id, name, phone, street, suburb, state, postcode, latitude, longitude, store_url, str(this_week), str(next_week)))
    db.commit()

    