#X-Originating-IP will give the IP of the original sender. Testing via personal email and Tunnel Bear.
#Not available under VPN, will look for a secondary way of doing it.
import json
import requests
from pprint import pprint

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def headerGet(iD, session):

    headerGrade=0
    
    nameSearch = 'X-Originating-IP'

    ipInformation = None

    mail_header_info = session.get(api_endpoint((f'me/messages/{iD}/?select=internetMessageHeaders')))

    mail_header = json.dumps(mail_header_info.json(), indent=4, sort_keys=True)

    print(28* ' ', "Grabbing IP information\n" )

    mail_header_json = json.loads(mail_header)

    length = len(mail_header_json['internetMessageHeaders'])

    for key in range(length):  
        if nameSearch == mail_header_json['internetMessageHeaders'][key]['name']:
            ipNoSplice = mail_header_json['internetMessageHeaders'][key]['value']
            ipInformation = ipNoSplice[1:-1]
        
    if ipInformation != None:
        print (ipInformation, '\n')

    else:
        print ('No IP found? Flagging.\n')
        headerGrade = headerGrade -1

    print (' Testing API to see location\n')

    ipApiInfoJson = requests.get(f'http://ip-api.com/json/{ipInformation}')

    ipApiInfo = json.dumps(ipApiInfoJson.json(), indent=4, sort_keys=True)

    print (ipApiInfo, '\n')

    ipInfoLoad = json.loads(ipApiInfo)

    print ('Checking Country\n')

    if ipInfoLoad['country'] == 'United States':
        print ('Country is United States, checking State\n')
        headerGrade = headerGrade +1

        if ipInfoLoad['regionName'] == 'Georgia':
            print ('State is Georgia, exiting loop.\n')
            headerGrade = headerGrade +1

    else:
        print('Country is not United States, flagging.\n')
        headerGrade = headerGrade -1



    if headerGrade == 0:
        print ('Uncertain about email origin status, leaving neutral.\n')
        print('Header Grade:',headerGrade, '\n')

    elif headerGrade>0:
        print ('Header seemingly is from a secure enviornment, positive review.\n')
        print('Header Grade:',headerGrade, '\n')

    elif headerGrade<0:
        print ('Header has failed test, giving negative mark.\n')
        print('Header Grade:',headerGrade, '\n')

    return headerGrade


