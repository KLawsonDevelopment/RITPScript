# This is a script designed to have an email sent to an inbox, parse said email for Header, To, From, and Body, send the information
# to other scripts that run one at a time to make the load easier, and feed True or False responses to a response email that gives
# a table to said sender if the email is good or not.
# This set of scripts is designed by Keith Lawson, and created while working for Rocket IT. If you need development help with this program,
# send an email to KLawsondevelopment@gmail.com or KLawson@rocketit.com 

#Importing all files to reference later

import pprint
import config
import json
import dataParsing
import time


from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def main_request(session):
    print('\nGet user unread messages -> https://graph.microsoft.com/v1.0/me/messages?$filter=isRead ne true')

    user_MAIL = session.get(api_endpoint('me/messages?$filter=isRead ne true'))

    print(28* ' ' + f'<Response [{user_MAIL.status_code}]>', f'bytes returned: {len(user_MAIL.text)}\n')

    print(30* ' ' + f'<Loading JSON into a readable format and grabbing IDs.')

    text = json.dumps(user_MAIL.json(), indent=4, sort_keys=True)

    print(32* ' ' + 'Printing value within JSON')

    json_object = json.loads(text)

    length = len(json_object['value'])

    idArray = []

    if length>0:
        for key in range(length):
            idArray.insert(key, json_object['value'][key]['id'])
            print (idArray)
            print (28* ' ', "ID BREAK\n")
        print (35* ' ', 'Beginning ID Loop\n')
        for key in range(length):
            dataParsing.dataGrab(idArray[key], session)
        main_request(session)
    else:
        print ('No ID found, looping around in 30 seconds to continue loop.\n')
        time.sleep(30)
        main_request(session)

        
    if not user_MAIL.ok:
        pprint.pprint(user_MAIL.json()) # display error
        return

    

if __name__ == '__main__':
    GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
    if GRAPH_SESSION:
        main_request(GRAPH_SESSION)

