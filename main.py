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
        # print (json_object['value'][key]['id'])
            idArray.insert(key, json_object['value'][key]['id'])
        # print (28* ' ', "BREAK")  
            print (idArray)
            print (28* ' ', "ID BREAK")
    else:
        print ('No ID Found, closing loop.')

    

    print (35* ' ', 'Beginning ID Loop')
    
    for key in range(length):
        dataParsing.dataGrab(idArray[key], session)



        
    if not user_MAIL.ok:
        pprint.pprint(user_MAIL.json()) # display error
        return

if __name__ == '__main__':
    GRAPH_SESSION = device_flow_session(config.CLIENT_ID)
    if GRAPH_SESSION:
        main_request(GRAPH_SESSION)

# def sendmail_sample(session):
#     """Send email from authenticated user.

#     session = requests.Session() instance with a valid access token for
#               Microsoft Graph in its default HTTP headers

#     This sample retrieves the user's profile photo, uploads it to OneDrive,
#     creates a view-only sharing link for the photo, and sends an email
#     with the photo attached.

#     The code in this function includes many print statements to provide
#     information about which endpoints are being called and the status and
#     size of Microsoft Graph responses. This information is helpful for
#     understanding how the sample works with Graph, but would not be included
#     in a typical production application.
#     """

#     print('\nGet user profile ---------> https://graph.microsoft.com/beta/me')
#     user_profile = session.get(api_endpoint('me'))
#     print(28*' ' + f'<Response [{user_profile.status_code}]>', f'bytes returned: {len(user_profile.text)}\n')
#     if not user_profile.ok:
#         pprint.pprint(user_profile.json()) # display error
#         return
#     user_data = user_profile.json()
#     email = user_data['mail']
#     display_name = user_data['displayName']

#     print(f'Your name ----------------> {display_name}')
#     print(f'Your email ---------------> {email}')
#     email_to = input(f'Send-to (ENTER=self) -----> ') or email

#     print('\nGet profile photo --------> https://graph.microsoft.com/beta/me/photo/$value')
#     photo, photo_status_code, _, profile_pic = profile_photo(session, save_as='me')
#     print(28*' ' + f'<Response [{photo_status_code}]>',
#           f'bytes returned: {len(photo)}, saved as: {profile_pic}')
#     if not 200 <= photo_status_code <= 299:
#         return


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