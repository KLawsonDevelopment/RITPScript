import json
from sys import breakpointhook
import requests
from pprint import pprint
import time
import re

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def respondToEmail(iD, session, headerGrade, toGrade, fromGrade, bodyGrade):

    headerGoB = str
    toGoB = str
    fromGoB = str
    bodyGoB = str

    if headerGrade > 0:
        headerGoB = 'Good'
    elif headerGrade == 0:
        headerGoB = 'Neutral'
    else:
        headerGoB = 'Bad'

    if toGrade > 0:
        toGoB = 'Good'
    elif toGrade == 0:
        toGoB = 'Neutral'
    else:
        toGoB = 'Bad'

    if fromGrade > 0:
        fromGoB = 'Good'
    elif fromGrade == 0:
        fromGoB = 'Neutral'
    else:
        fromGoB = 'Bad'

    if bodyGrade > 0:
        bodyGoB = 'Good'
    elif bodyGrade == 0:
        bodyGoB = 'Neutral'
    else:
        bodyGoB = 'Bad'

    totalArray =[]
    totalArray.append(headerGoB)
    totalArray.append(toGoB)
    totalArray.append(fromGoB)
    totalArray.append(bodyGoB)

    immediateFail = totalArray.count('Bad')

    totalGrade = headerGrade + toGrade + fromGrade + bodyGrade

    goodOrBad = str

    if immediateFail > 1:
        goodOrBad = 'We believe this email should not be opened.'
    elif totalGrade > 0:
        goodOrBad = 'This email should be safe to open.'
    elif totalGrade == 0:
        goodOrBad = 'We are not sure if this email is safe to open.'
    else:
        goodOrBad = 'We believe this email should not be opened.'



    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    to_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    to_data_json = json.loads(to_data)

    email_to = to_data_json['sender']['emailAddress']['address']

    with open('email.html') as template_file:
        template = template_file.read().format(headerGrade=headerGrade, toGrade=toGrade, fromGrade=fromGrade, bodyGrade=bodyGrade,
                                                headerGoB=headerGoB, toGoB=toGoB, fromGoB=fromGoB, bodyGoB=bodyGoB, goodOrBad=goodOrBad)

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

    return