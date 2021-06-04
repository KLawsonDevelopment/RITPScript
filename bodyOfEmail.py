import json
import requests
from pprint import pprint
import time

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file

def bodyGet(iD, session):
    bodyGrade = 0

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    body_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    body_data_json = json.loads(body_data)

    pprint(body_data)