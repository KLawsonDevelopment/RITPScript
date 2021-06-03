#X-Originating-IP will give the IP of the original sender. Testing via personal email and Tunnel Bear.
#Not available under VPN, will look for a secondary way of doing it.

import json
import re

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def headerGet(iD, session):
    mail_header_info = session.get(api_endpoint((f'me/messages/{iD}/?select=internetMessageHeaders')))

    mail_header = json.dumps(mail_header_info.json(), indent=4, sort_keys=True)

    print(28* ' ', "Grabbing IP information\n" )

    mail_header_json = json.loads(mail_header)

    # ipInformation = mail_header['internetMessageHeaders']['X-Originating-IP']

    # print (mail_header_json['internetMessageHeaders'][20]['name'])

    nameSearch = 'X-Originating-IP'

    ipInformation = None

    length = len(mail_header_json['internetMessageHeaders'])

    for key in range(length):  
        if nameSearch == mail_header_json['internetMessageHeaders'][key]['name']:
            ipInformation = mail_header_json['internetMessageHeaders'][key]['value']
        
    if ipInformation != None:
        print (ipInformation, '\n')
    else:
        print ('No IP found? Flagging.\n')

