import json
import re
from pprint import pprint
import time

from helpers import api_endpoint

def fromGet(iD, session):

    #Create fromGrade to return to dataParsing, toAddress and fromAddress are initialized early to avoid not defined errors

    fromGrade = 0

    toAddress = str

    fromAddress = str

    #Get email data from ID and load into a DICT

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    from_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    from_data_json = json.loads(from_data)

    # Search for specific parts of emails like if they are forwarded or are from the ticket system, and look for original senders. This part gets a lot adjusted and added to due to different types of emails arriving all the time.

    if '-----Original Message-----' in from_data_json['body']['content']:
        print('Checking "Original Message"\n')
        body_data_json = json.dumps(from_data_json['body']['content'].rsplit('-----Original Message-----', 1)[1])
        body_data_json = json.loads(body_data_json)

        if 'From:' in body_data_json:
            print('Checking "From"\n')
            if '.edu' in body_data_json:
                fromAddress = body_data_json.split('@',1)[1].split('.edu')[0]

            elif '.com' in body_data_json:
                fromAddress = body_data_json.split('@',1)[1].split('.com')[0]

            elif '.net' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.net')[0]

            elif '.org' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.org')[0]

            elif '.gov' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.gov')[0]

            elif '.mil' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.mil')[0]  
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

            if '.edu' in body_data_json:
                fromAddress = body_data_json.split('@',1)[1].split('.edu')[0]

            elif '.com' in body_data_json:
                fromAddress = body_data_json.split('@',1)[1].split('.com')[0]

            elif '.net' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.net')[0]

            elif '.org' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.org')[0]

            elif '.gov' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.gov')[0]

            elif '.mil' in body_data_json:
                fromAddress = body_data_json.split('@', 1)[1].split('.mil')[0]  

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

        if '.edu' in body_data_json:
            fromAddress = body_data_json.split('@',1)[1].split('.edu')[0]

        elif '.com' in body_data_json:
            fromAddress = body_data_json.split('@',1)[1].split('.com')[0]

        elif '.net' in body_data_json:
            fromAddress = body_data_json.split('@', 1)[1].split('.net')[0]

        elif '.org' in body_data_json:
            fromAddress = body_data_json.split('@', 1)[1].split('.org')[0]

        elif '.gov' in body_data_json:
            fromAddress = body_data_json.split('@', 1)[1].split('.gov')[0]

        elif '.mil' in body_data_json:
            fromAddress = body_data_json.split('@', 1)[1].split('.mil')[0]                                    
        
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

    #Open the domains list and read each line, then load it into a dict so I can check it later.
    
    domainFile = open('domains.txt', 'r')
    checkDomain = domainFile.read().splitlines()
    domainLength = len(checkDomain)

    #For loop that if the fromAddress and the loaded checkDomain DICT have any matches, move on to if statement below.
    
    for line in range(domainLength):
        z = re.match(fromAddress, checkDomain[line])
        if z:
            break


            # If Z exists, it is safe due to it being in the domain list
            # if the addresses match, the org is the same and it should be safe.

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