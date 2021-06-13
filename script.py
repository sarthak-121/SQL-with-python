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
    Store_URL varchar(100)
)''')

mycursor.execute('''create table store_opening_time_next_week (
    Id int primary key,
    Monday varchar(50),
    Tuesday varchar(50),
    Wednesday varchar(50),
    Thursday varchar(50),
    Friday varchar(50),
    Saturday varchar(50),
    Sunday varchar(50)
)''')

mycursor.execute('''create table store_opening_time_current_week (
    Id int primary key,
    Monday varchar(50),
    Tuesday varchar(50),
    Wednesday varchar(50),
    Thursday varchar(50),
    Friday varchar(50),
    Saturday varchar(50),
    Sunday varchar(50)
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

    this_monday = this_week['Monday']
    this_tuesday = this_week['Tuesday']
    this_wednesday = this_week['Wednesday']
    this_thursday = this_week['Thursday']
    this_friday = this_week['Friday']
    this_saturday = this_week['Saturday']
    this_sunday = this_week['Sunday']

    next_monday = next_week['Monday']
    next_tuesday = next_week['Tuesday']
    next_wednesday = next_week['Wednesday']
    next_thursday = next_week['Thursday']
    next_friday = next_week['Friday']
    next_saturday = next_week['Saturday']
    next_sunday = next_week['Sunday']

    mycursor.execute('''INSERT INTO store_info (Id,Store_Name,Phone,street,suburb,state,postcode,Latitude,Longitude,Store_URL) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (id, name, phone, street, suburb, state, postcode, latitude, longitude, store_url))
    mycursor.execute('''INSERT INTO store_opening_time_current_week (ID,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', (id,this_monday,this_tuesday,this_wednesday,this_thursday,this_friday,this_saturday,this_sunday))
    mycursor.execute('''INSERT INTO store_opening_time_next_week (ID,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', (id,next_monday,next_tuesday,next_wednesday,next_thursday,next_friday,next_saturday,next_sunday))
    
    db.commit()

    