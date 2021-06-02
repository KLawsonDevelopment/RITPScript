# This is a script designed to have an email sent to an inbox, parse said email for Header, To, From, and Body, send the information
# to other scripts that run one at a time to make the load easier, and feed True or False responses to a response email that gives
# a table to said sender if the email is good or not.
# This set of scripts is designed by Keith Lawson, and created while working for Rocket IT. If you need development help with this program,
# send an email to KLawsondevelopment@gmail.com or KLawson@rocketit.com 

#Importing all files to reference later

import pprint
import config
import requests
import headerOfEmail
import to_sender
import from_sender 
import bodyOfEmail
import responseToEmail

from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file




def sendmail_sample(session):
    """Send email from authenticated user.

    session = requests.Session() instance with a valid access token for
              Microsoft Graph in its default HTTP headers

    This sample retrieves the user's profile photo, uploads it to OneDrive,
    creates a view-only sharing link for the photo, and sends an email
    with the photo attached.

    The code in this function includes many print statements to provide
    information about which endpoints are being called and the status and
    size of Microsoft Graph responses. This information is helpful for
    understanding how the sample works with Graph, but would not be included
    in a typical production application.
    """

    print('\nGet user profile ---------> https://graph.microsoft.com/beta/me')
    user_profile = session.get(api_endpoint('me'))
    print(28*' ' + f'<Response [{user_profile.status_code}]>', f'bytes returned: {len(user_profile.text)}\n')
    if not user_profile.ok:
        pprint.pprint(user_profile.json()) # display error
        return
    user_data = user_profile.json()
    email = user_data['mail']
    display_name = user_data['displayName']

    print(f'Your name ----------------> {display_name}')
    print(f'Your email ---------------> {email}')
    email_to = input(f'Send-to (ENTER=self) -----> ') or email

    print('\nGet profile photo --------> https://graph.microsoft.com/beta/me/photo/$value')
    photo, photo_status_code, _, profile_pic = profile_photo(session, save_as='me')
    print(28*' ' + f'<Response [{photo_status_code}]>',
          f'bytes returned: {len(photo)}, saved as: {profile_pic}')
    if not 200 <= photo_status_code <= 299:
        return

if __name__ == '__main__':
    GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
    if GRAPH_SESSION:
        sendmail_sample(GRAPH_SESSION)

# arg = "I am "
# word = 'no'

# response = requests.get("https://api.publicapis.org/entries")
# print (response.json())

#Generic call function with argument to test data passing

# arg seems to be set in While and MUST BE CHANGED WHILE INSIDE WHILE, cannot be changed by argument
# True or False seems to be a good flag system that can pass data along parameters, will be good to use for email response



#print ('On Main')
#while arg == 'I am ':
 #   headerOfEmail.test_para(arg)
 #   to_sender.test_para(arg)
 #   from_sender.test_para(arg)
 #   bodyOfEmail.test_para(arg)
 #   responseToEmail.test_para(arg)

  #  if responseToEmail.trueOrFalse(word)==True:
  #      print("True")
  #  elif responseToEmail.trueOrFalse(word)==False:
  #      print("False")
  #  else:
  #      print('N/A')##

   # arg='end'