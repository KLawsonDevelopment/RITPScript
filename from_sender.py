import json
import requests
from pprint import pprint
import time

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def fromGet(iD, session):
    fromGrade = 0

    toAddress = str

    fromAddress = str

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    from_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    from_data_json = json.loads(from_data)

    print('Checking sender data. \n')

    time.sleep(1)

    if from_data_json['toRecipients'] == []:
        pprint(from_data_json['toRecipients'])
    else:
        pprint(from_data_json['toRecipients'][0]['emailAddress']['address'])
        toAddress = from_data_json['toRecipients'][0]['emailAddress']['address'].split("@")[1]
        print (toAddress, '\n')
    if from_data_json['from'] == []:
        pprint(from_data_json['from'])
    else:
        pprint(from_data_json['from']['emailAddress']['address'])
        fromAddress = from_data_json['from']['emailAddress']['address'].split("@")[1]
        print(fromAddress, '\n')

    if fromAddress == toAddress:
        print('Same address, same org. Good sign.\n')
        fromGrade = fromGrade +1

    # PUT AN ELIF HERE WITH THE ORG DOMAINS LISTED

    else:
        print('Not same address, not same org. Bad sign.\n')
        fromGrade = fromGrade -1

    print('From Grade:', fromGrade, '\n')

    return fromGrade