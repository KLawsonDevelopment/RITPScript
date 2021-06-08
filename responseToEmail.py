import json
from sys import breakpointhook
import requests
from pprint import pprint
import time
import re

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def respondToEmail(iD, session, headerGrade, toGrade, fromGrade, bodyGrade):

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    to_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    to_data_json = json.loads(to_data)

    email_to = to_data_json['sender']['emailAddress']['address']

    with open('email.html') as template_file:
        template = template_file.read().format(headerGrade=headerGrade, toGrade=toGrade, fromGrade=fromGrade, bodyGrade=bodyGrade)

    send_response = send_mail(session=session,
                              subject='Results of your Phishing Email',
                              recipients=email_to.split(';'),
                              body=template)
    print(28*' ' + f'<Response [{send_response.status_code}]>')
    if not send_response.ok:
        pprint.pprint(send_response.json()) # show error message

    patchRequest = {'isRead': True}

    isMessageRead = session.patch(api_endpoint(f'me/messages/{iD}'),
                                headers={'Content-Type': 'application/json'},
                                json = patchRequest)

    print('Did Message Patch:',isMessageRead)
