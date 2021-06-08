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

    if '-----Original Message-----' in from_data_json['body']['content']:
        body_data_json = json.dumps(from_data_json['body']['content'].split('-----Original Message-----', 1)[1])
        body_data_json = json.loads(body_data_json)

        if 'From:' in body_data_json:
            fromAddress= body_data_json.split('From: ', 1)[1].split('@')[1].split('>')[0]
            pprint(fromAddress)
            if from_data_json['toRecipients'] == []:
                pprint(from_data_json['toRecipients'])
            else:
                pprint(from_data_json['toRecipients'][0]['emailAddress']['address'])
                toAddress = from_data_json['toRecipients'][0]['emailAddress']['address'].split("@")[1]
                print (toAddress, '\n')

        else:
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



    time.sleep(1)

    
    print('Checking sender data. \n')
    


    if fromAddress == toAddress:
        print('Same address, same org. Good sign.\n')
        fromGrade = fromGrade +1

    # PUT AN ELIF HERE WITH THE ORG DOMAINS LISTED

    else:
        print('Not same address, not same org. Bad sign.\n')
        fromGrade = fromGrade -1

    print('From Grade:', fromGrade, '\n')

    return fromGrade