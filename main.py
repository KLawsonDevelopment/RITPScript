# This is a script designed to have an email sent to an inbox, parse said email for Header, To, From, and Body, send the information
# to other scripts that run one at a time to make the load easier, and feed True or False responses to a response email that gives
# a table to said sender if the email is good or not.
# This set of scripts is designed by Keith Lawson, and created while working for Rocket IT. If you need development help with this program,
# send an email to KLawsondevelopment@gmail.com or KLawson@rocketit.com 

from logging import exception
import requests
import config
import json
import dataParsing
import time




# importing from the helpers file that Microsoft provides to help with API talking


from helpers import api_endpoint, device_flow_session

def main_request(session):

    #Creating a Time variable so I can see when the script last looped

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S")

    #Calling API with the filter that looks for any unread emails.

    print('\nGet user unread messages -> https://graph.microsoft.com/v1.0/me/messages?$filter=isRead ne true')
    
    while True:
        try:
            user_MAIL = session.get(api_endpoint('me/messages?$filter=isRead ne true'))
            break
        except (requests.exceptions.RequestException, ValueError):
            print("Timeout Occurred")
            pass
    #Success or failure status code from the JSON

    print(28* ' ' + f'<Response [{user_MAIL.status_code}]>', f'bytes returned: {len(user_MAIL.text)}\n')

    # user_MAIL.status_code = 401

    if user_MAIL.status_code == '401':
        print(38* '', 'Token has expired, attempting to get new one. String exception.\n')
        GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
        if GRAPH_SESSION:
            main_request(GRAPH_SESSION)

    elif user_MAIL.status_code == [401]:
        print(38* '', 'Token has expired, attempting to get new one. Array exception.\n')
        GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
        if GRAPH_SESSION:
            main_request(GRAPH_SESSION)

    elif user_MAIL.status_code == 401:
        print(38* '', 'Token has expired, attempting to get new one. Integer exception.\n')
        GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
        if GRAPH_SESSION:
            main_request(GRAPH_SESSION)

    print(30* ' ' + f'<Loading JSON into a readable format and grabbing IDs.')

    text = json.dumps(user_MAIL.json(), indent=4, sort_keys=True)

    #Loading text into a python directory to grab data as needed

    json_object = json.loads(text)

    #Created a length for a for loop so that the IDs can loop properly

    length = len(json_object['value'])

    #Made and array/list to actually hold the JSON data

    idArray = []

    # If statement checking to see if any IDs have been found. If an ID is found, loop through each key one by one. If no ID is found, loop the script after 30 seconds.

    if length>0:

        #For loop begins here. Grabbing the ID, putting it into the array, printing what IDs are there.

        for key in range(length):
            idArray.insert(key, json_object['value'][key]['id'])
            print (idArray)
            print (28* ' ', "ID BREAK\n")
        print (35* ' ', 'Beginning ID Loop\n')

        #Loop through each individual key by going to Data Parsing.

        for key in range(length):
            dataParsing.dataGrab(idArray[key], session)
        main_request(session)
    else:
        print ('No ID found, looping around in 30 seconds to continue loop.\n')
        print ('Time:', current_time)
        time.sleep(30)
        main_request(session)

        
    if not user_MAIL.ok:
        main_request(session)
        # pprint.pprint(user_MAIL.json()) # display error
        return

    

if __name__ == '__main__':
    GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
    if GRAPH_SESSION:
        main_request(GRAPH_SESSION)

