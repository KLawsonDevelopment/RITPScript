import json
import time

from helpers import api_endpoint

def toGet(iD, session):

    #Create toGrade to return to dataParsing

    toGrade = 0

    #Get mail information via ID, and load into a DICT

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    to_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    to_data_json = json.loads(to_data)

    #Create length based on dict

    length = len(to_data_json['toRecipients'])

    print('Checking reviever data. \n')

    time.sleep(1)

    #If the length is 0, assume a bad email. If not, assume email is fine.

    if length == 0:
        print('No recipients found, flag.\n')
        toGrade = toGrade - 1
    else:
        print('More than 0 recipients found.\n')
        toGrade = toGrade +1

    #Return toGrade

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