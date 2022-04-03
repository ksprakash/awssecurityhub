from datetime import datetime
#import pytz

def convert_from_str_date(dtstr):
    #date = datetime.strptime(dtstr,"%Y-%m-%dT%H:%M:%S.%fZ").astimezone(tz=pytz.timezone('UTC'))
    date = datetime.strptime(dtstr,"%Y-%m-%dT%H:%M:%S.%fZ")
    return date

def change_name_lower(name: str) -> str:
    name = name.lower()
    return name
