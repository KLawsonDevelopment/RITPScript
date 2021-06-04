import json
import requests
from pprint import pprint

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def toGet(iD, session):
    toGrade = 0

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    to_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    to_data_json = json.loads(to_data)

    length = len(to_data_json['toRecipients'])

    if length == 0:
        print('No recipients found, flag.\n')
        toGrade = toGrade - 1
    else:
        print('More than 0 recipients found.\n')
        toGrade = toGrade +1

    if toGrade == 0:
        print ('Uncertain about recipient status, leaving neutral.\n')
        print ('To Grade:', toGrade, '\n')
    
    elif toGrade > 0:
        print ('Recipient status is positive, good sign.\n')
        print('To Grade:', toGrade, '\n')
    
    elif toGrade < 0:
        print ('Recipient grade is negative, flagging.\n')
        print ('To Grade:', toGrade, '\n')

    return toGrade