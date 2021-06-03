# Used from Microsoft, able to be copied and used at will under MIT License, per Microsoft

"""Configuration settings for console app using device flow authentication
"""

CLIENT_ID = 'dcde5c47-90ef-4fbc-acae-07a616c1c6d6'

AUTHORITY_URL = 'https://login.microsoftonline.com/common'
RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'v1.0'

# This code can be removed after configuring CLIENT_ID and CLIENT_SECRET above.
if 'ENTER_YOUR' in CLIENT_ID:
    print('ERROR: config.py does not contain valid CLIENT_ID.')
    import sys
    sys.exit(1)