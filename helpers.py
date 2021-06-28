"""helper functions for Microsoft Graph"""
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
import base64
import mimetypes
import urllib
import time
from sys import platform

from adal import AuthenticationContext
import pyperclip
import requests

import config

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Enter Code : otc, paste code here
# Submit button for Code: idSIButton9
# Email: i0116, not listing here.
# Submit button for Email : idSIButton9
# Password: i0118, not listing here.
# Submit button for Password: idSIButton9
# Test Phishing: table, click
# Submit button for Sign In: idSIButton9


ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
submitButton = 'idSIButton9'
file = open('(oolAmber91.txt')
lines = file.readlines()
email = lines[0]
passW = lines[1]

def api_endpoint(url):
    """Convert a relative path such as /me/photo/$value to a full URI based
    on the current RESOURCE and API_VERSION settings in config.py.
    """

    time.sleep(2)
    if urllib.parse.urlparse(url).scheme in ['http', 'https']:
        return url # url is already complete

    return urllib.parse.urljoin(f'{config.RESOURCE}/{config.API_VERSION}/',
                                url.lstrip('/'))



def device_flow_session(client_id, auto=True):
    """Obtain an access token from Azure AD (via device flow) and create
    a Requests session instance ready to make authenticated calls to
    Microsoft Graph.

    client_id = Application ID for registered "Azure AD only" V1-endpoint app
    auto      = whether to copy device code to clipboard and auto-launch browser

    Returns Requests session object if user signed in successfully. The session
    includes the access token in an Authorization header.

    User identity must be an organizational account (ADAL does not support MSAs).
    """
    ctx = AuthenticationContext(config.AUTHORITY_URL, api_version=None)
    device_code = ctx.acquire_user_code(config.RESOURCE,
                                        client_id)

    # display user instructions
    if auto:
        pyperclip.copy(device_code['user_code']) # copy user code to clipboard
        # webbrowser.open(device_code['verification_url']) # open browser
        print(f'The code {device_code["user_code"]} has been copied to your clipboard, '
              f'and your web browser is opening {device_code["verification_url"]}. '
              'Paste the code to sign in.')

        # elif statement to check system to run proper geckodriver

        if platform == 'darwin':
            driver = webdriver.Firefox(executable_path='./geckodriverOSX')
        elif platform == 'win64':
            driver = webdriver.Firefox(executable_path='./geckodriver64')
        elif platform == 'win32':
            driver = webdriver.Firefox(executable_path='./geckodriver32')

        #Open Driver
        
        driver.get('https://microsoft.com/devicelogin')
        time.sleep(5)

        #Interface with driver to input: User Code, Username, and Password
        
        print('Sending code\n')

        web_interface('otc', device_code['user_code'], 'MFA Code', driver)

        time.sleep(5)

        web_interface('i0116', email, 'email', driver)

        time.sleep(5)

        web_interface('i0118', passW, 'password', driver)

        time.sleep(5)

        submit_web(driver)

        time.sleep(5)

        driver.close()

    else:
        print(device_code['message'])

    token_response = ctx.acquire_token_with_device_code(config.RESOURCE,
                                                        device_code,
                                                        client_id)
    if not token_response.get('accessToken', None):
        return None

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {token_response["accessToken"]}',
                            'SdkVersion': 'sample-python-adal',
                            'x-client-SKU': 'sample-python-adal'})
    return session


def send_mail(session, *, subject, recipients, body='', content_type='HTML',
              attachments=None):
    """Send email from current user.

    session      = requests.Session() instance with Graph access token
    subject      = email subject (required)
    recipients   = list of recipient email addresses (required)
    body         = body of the message
    content_type = content type (default is 'HTML')
    attachments  = list of file attachments (local filenames)

    Returns the response from the POST to the sendmail API.
    """

    # Create recipient list in required format.
    recipient_list = [{'EmailAddress': {'Address': address}}
                      for address in recipients]

    # Create list of attachments in required format.
    attached_files = []
    if attachments:
        for filename in attachments:
            b64_content = base64.b64encode(open(filename, 'rb').read())
            mime_type = mimetypes.guess_type(filename)[0]
            mime_type = mime_type if mime_type else ''
            attached_files.append( \
                {'@odata.type': '#microsoft.graph.fileAttachment',
                 'ContentBytes': b64_content.decode('utf-8'),
                 'ContentType': mime_type,
                 'Name': filename})

    # Create email message in required format.
    email_msg = {'Message': {'Subject': subject,
                             'Body': {'ContentType': content_type, 'Content': body},
                             'ToRecipients': recipient_list,
                             'Attachments': attached_files},
                 'SaveToSentItems': 'true'}

    # Do a POST to Graph's sendMail API and return the response.
    return session.post(api_endpoint('me/microsoft.graph.sendMail'),
                        headers={'Content-Type': 'application/json'},
                        json=email_msg)

def web_interface(element, text, target, driver):

    actions = ActionChains(driver)

    print('Inputting', target, '\n')

    Elem = WebDriverWait(driver, timeout=10, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, element)))
    submitElem = WebDriverWait(driver, timeout=10, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, submitButton)))
    
    Elem.clear()
    actions.move_to_element(Elem)
    actions.click(Elem)
    actions.send_keys(text)
    actions.move_to_element(submitElem)
    actions.click(submitElem)
    actions.perform()
    

def submit_web(driver):
    actions = ActionChains(driver)

    submitElem = WebDriverWait(driver, timeout=10, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, submitButton)))

    
    actions.move_to_element(submitElem)
    actions.click(submitElem)
    actions.perform()