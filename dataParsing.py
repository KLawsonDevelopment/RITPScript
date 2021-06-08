import headerOfEmail
import to_sender
import from_sender 
import bodyOfEmail
import responseToEmail
import json
import time

from headerOfEmail import *

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def dataGrab(iD, session):

    print('ID Loop, ID used:', iD, '\n')

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    mail_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    print ('Calling for Header via Script\n')

    time.sleep(3)

    headerGrade = headerOfEmail.headerGet(iD, session)

    print ('Calling for To via Script\n')

    time.sleep(3)

    toGrade = to_sender.toGet(iD, session)

    print ('Calling for From via Script\n')

    time.sleep(3)

    fromGrade = from_sender.fromGet(iD, session)

    print ('Calling for Body via Script\n')

    time.sleep(3)

    bodyGrade = bodyOfEmail.bodyGet(iD, session)

    print ('Calling for Response via Script')

    time.sleep(3)

    responseToEmail.respondToEmail(iD, session, headerGrade, toGrade, fromGrade, bodyGrade)