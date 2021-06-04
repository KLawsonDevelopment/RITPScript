import inspect
import requests
import headerOfEmail
import to_sender
import from_sender 
import bodyOfEmail
import responseToEmail
import json

from headerOfEmail import *

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def dataGrab(iD, session):

    print('ID Loop, ID used:', iD)

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    mail_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    print ('Calling Header via Script\n')

    headerGrade = headerOfEmail.headerGet(iD, session)

    toGrade = to_sender.toGet(iD, session)

    from_sender.fromGet(iD, session)