### Data Parsing is the main section of the script. It handles getting the 'grades' of each part of the email that is applicable, loading that data into variables, and sending a response.

#Importing all other parts of the script, along with json and time to handle data and timing respectively

import headerOfEmail
import to_sender
import from_sender 
import bodyOfEmail
import responseToEmail
import json
import time

from headerOfEmail import *

from helpers import api_endpoint

#Main function. This goes through each other part of the script and gets the grades as needed.

def dataGrab(iD, session):

    #Same idea as main.py, grabbing the JSON for the related ID in this section.

    print('ID Loop, ID used:', iD, '\n')

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    mail_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    #This calls the to_sender script, and the fucntion toGet.

    print ('Calling for To via Script\n')

    time.sleep(3)

    toGrade = to_sender.toGet(iD, session)

    # Below calls the from_sender script, and the fromGet function

    print ('Calling for From via Script\n')

    time.sleep(3)

    fromGrade = from_sender.fromGet(iD, session)

    # Slightly different logic for the headerGrade. If the From script fails, it immediately fails the header grade as it originated from outside of the organization and cannot be a good header.
    # If I get the ability to domain check this logic will be adjusted.

    if fromGrade <0:
        print('Failing Header Grade due to From Grade failing\n')
        headerGrade = -1
    else:
        print ('Calling for Header via Script\n')

        time.sleep(3)

        headerGrade = headerOfEmail.headerGet(iD, session)

    # Below calls the bodyOfEmail script, and the bodyGet function.

    print ('Calling for Body via Script\n')

    time.sleep(3)

    bodyGrade = bodyOfEmail.bodyGet(iD, session)


    # Below calls the responseToEmail script, and the respondToEmail function

    print ('Calling for Response via Script')

    time.sleep(3)

    responseToEmail.respondToEmail(iD, session, headerGrade, toGrade, fromGrade, bodyGrade)

    return