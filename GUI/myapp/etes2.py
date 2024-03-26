import requests
import ujson as json
from datetime import datetime
import time
# print(len(data[0]['today'][0]))
update_event_name = ""
update_event_date = ""
update_event_time = ""
update_event_desc = ""
update_event_id   = ""

def get_current_event_data(update,data: list):
    global update_event_name, update_event_date, update_event_time, update_event_desc, update_event_id
    try:

        if len(data[0][f'{update}'][0]) > 0:
            # print(f"{update} Event ")
            update_event_name = data[0][f'{update}'][0]['eventName']
            dt_obj=  data[0][f'{update}'][0]['eventStartDate']
            update_event_date ,update_event_time = dt_obj.split('T')
            update_event_time = update_event_time.rstrip('Z')
            update_event_desc = data[0][f'{update}'][0]['eventDescription']
            update_event_id = data[0][f'{update}'][0]['_id']
            print(update_event_name)        # Comment out this after testing
            print(update_event_date)        # Comment out this after testing
            print(update_event_time)        # Comment out this after testing
            print(update_event_desc)        # Comment out this after testing
            print(update_event_id)        # Comment out this after testing
    except Exception as e:
        print(e)

def check_event():
    try:
        response = requests.get('https://api.npoint.io/ac84ca141e388bf2bb9c')
        data = response.json()
        if len(data[0]['today'][0]) > 0:
            get_current_event_data("today",data)
        elif len(data[0]['tomorrow'][0]) > 0:
            get_current_event_data("tomorrow",data)
        elif len(data[0]['upcoming'][0]) > 0:
            get_current_event_data("upcoming",data)
    except Exception as e:
        print(e)

check_event()
