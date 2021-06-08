import json
from sys import breakpointhook
import requests
from pprint import pprint
import time
import re

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def bodyGet(iD, session):
    bodyGrade = 0

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    body_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    body_data_json = json.loads(body_data)

    #disgusting regex below

    hyperLinks = re.findall(r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b', body_data_json['body']['content'])

    length = len(hyperLinks)

    print(hyperLinks)

    print('Checking for matches\n')

    domainFile = open('domains.txt', 'r')
    checkDomain = domainFile.read().splitlines()
    domainLength = len(checkDomain)
    comCheck = '.com'

    for link in range(length):
        for line in range(domainLength):
            hyperLinks[link] = hyperLinks[link].replace("http://www.", '')
            hyperLinks[link] = hyperLinks[link].replace('https://www.', '')
            hyperLinks[link] = hyperLinks[link].replace('https://', '')
            hyperLinks[link] = hyperLinks[link].replace('www.', '')
            hyperLinks[link] = hyperLinks[link].split(comCheck, 1)[0]
            z = re.match(hyperLinks[link], checkDomain[line])
            if z:
                print(hyperLinks[link])
                print(checkDomain[line])
                print('match\n')
                bodyGrade = bodyGrade+1
                break
            elif line == domainLength - 1: 
                bodyGrade = bodyGrade - 1

    print('Body Grade:',bodyGrade,'\n')

    return bodyGrade