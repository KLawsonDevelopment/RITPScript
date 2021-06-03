import inspect
import requests
import headerOfEmail
import to_sender
import from_sender 
import bodyOfEmail
import responseToEmail
import json

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def dataGrab(iD, session):
    print('ID Loop, ID used:', iD)

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    mail_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)


    print ('Calling Header via Script\n')

    headerOfEmail.headerGet(iD, session)

#   headerOfEmail.test_para(arg)
#   to_sender.test_para(arg)
#   from_sender.test_para(arg)
#   bodyOfEmail.test_para(arg)
#   responseToEmail.test_para(arg)