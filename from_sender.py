import json
import requests
import re
from pprint import pprint
import time

from helpers import api_endpoint

def fromGet(iD, session):
    fromGrade = 0

    toAddress = str

    fromAddress = str

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    from_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    from_data_json = json.loads(from_data)

    if '-----Original Message-----' in from_data_json['body']['content']:
        print('Checking "Original Message"\n')
        body_data_json = json.dumps(from_data_json['body']['content'].rsplit('-----Original Message-----', 1)[1])
        body_data_json = json.loads(body_data_json)

        if 'From:' in body_data_json:
            print('Checking "From"\n')
            fromAddress= body_data_json.rsplit('From: ', 1)[1].split('@')[1].split('>')[0]
            pprint(fromAddress)

            if from_data_json['toRecipients'] == []:
                pprint(from_data_json['toRecipients'])
            else:
                pprint(from_data_json['toRecipients'][0]['emailAddress']['address'])
                toAddress = from_data_json['toRecipients'][0]['emailAddress']['address'].split("@")[1]
                print (toAddress, '\n')



    elif 'FW:' in from_data_json['body']['content']:
        print('Checking "FW"\n')
        body_data_json = json.dumps(from_data_json['body']['content'].rsplit('FW:',1)[1])
        body_data_json = json.loads(body_data_json)
        print(body_data_json)

        if 'From:' in body_data_json:
            print('Checking "From"\n')
            fromAddress = body_data_json.split('From:')[1].split('@')[1].split('>')[0]
            pprint(fromAddress)
            if from_data_json['toRecipients'] == []:
                pprint(from_data_json['toRecipients'])
            else:
                pprint(from_data_json['toRecipients'][0]['emailAddress']['address'])
                toAddress = from_data_json['toRecipients'][0]['emailAddress']['address'].split("@")[1]
                print (toAddress, '\n')

    elif 'From:' in from_data_json['body']['content']:
        print("Checking 'From'\n")
        body_data_json = json.dumps(from_data_json['body']['content'].rsplit('From:',1)[1])
        body_data_json = json.loads(body_data_json)
        print(body_data_json)
        fromAddress = body_data_json.rsplit('@',1)[1].split('.com')[0]
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
    
    domainFile = open('domains.txt', 'r')
    checkDomain = domainFile.read().splitlines()
    domainLength = len(checkDomain)
    
    for line in range(domainLength):
        z = re.match(fromAddress, checkDomain[line])
        if z:
            break

    if z:
        print('Address found in the Domain List, safe.\n')
        fromGrade = fromGrade +1

    elif fromAddress == toAddress:
        print('Same address, same org. Good sign.\n')
        fromGrade = fromGrade +1

    else:
        print('Not same address, not same org. Bad sign.\n')
        fromGrade = fromGrade -1

    print('From Grade:', fromGrade, '\n')

    return fromGrade