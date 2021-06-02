# This is a script designed to have an email sent to an inbox, parse said email for Header, To, From, and Body, send the information
# to other scripts that run one at a time to make the load easier, and feed True or False responses to a response email that gives
# a table to said sender if the email is good or not.
# This set of scripts is designed by Keith Lawson, and created while working for Rocket IT. If you need development help with this program,
# send an email to KLawsondevelopment@gmail.com or KLawson@rocketit.com 

#Importing all files to reference later

import requests
import headerOfEmail
import to_sender
import from_sender 
import bodyOfEmail
import responseToEmail




arg = "I am "
word = 'no'

response = requests.get("https://api.publicapis.org/entries")
print (response.json())

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