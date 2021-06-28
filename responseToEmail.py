import json
from pprint import pprint

from helpers import api_endpoint, send_mail

def respondToEmail(iD, session, headerGrade, toGrade, fromGrade, bodyGrade):

    #Create GoodorBad variables to shove strings into for the HTML.

    headerGoB = str
    toGoB = str
    fromGoB = str
    bodyGoB = str

    #Repetitive if statement to verify what is good or bad, and set variables so that the HTML can set it properly.

    if headerGrade > 0:
        headerGoB = 'Good'
    elif headerGrade == 0:
        headerGoB = 'Neutral'
    else:
        headerGoB = 'Bad'

    if toGrade > 0:
        toGoB = 'Good'
    elif toGrade == 0:
        toGoB = 'Neutral'
    else:
        toGoB = 'Bad'

    if fromGrade > 0:
        fromGoB = 'Good'
    elif fromGrade == 0:
        fromGoB = 'Neutral'
    else:
        fromGoB = 'Bad'

    if bodyGrade > 0:
        bodyGoB = 'Good'
    elif bodyGrade == 0:
        bodyGoB = 'Neutral'
    else:
        bodyGoB = 'Bad'

    #Created an Array/DICT that searches for how many Bad checks there are.

    totalArray =[]
    totalArray.append(headerGoB)
    totalArray.append(toGoB)
    totalArray.append(fromGoB)
    totalArray.append(bodyGoB)

    immediateFail = totalArray.count('Bad')

    #Add together all of the grades.

    totalGrade = headerGrade + toGrade + fromGrade + bodyGrade

    goodOrBad = str

    #If Immediate Fail counts over 1 Bad in the email, fail it.
    # If TotalGrade is above 0, it *should* be safe to open.
    # If it's 0, say we do not know.
    # If it's below 0, say it is not to be opened.

    if immediateFail > 1:
        goodOrBad = 'We believe this email should not be opened.'
    elif totalGrade > 0:
        goodOrBad = 'This email should be safe to open.'
    elif totalGrade == 0:
        goodOrBad = 'We are not sure if this email is safe to open.'
    else:
        goodOrBad = 'We believe this email should not be opened.'

    # Get the mail data from the API/ID.

    mail_data_get = session.get(api_endpoint((f'me/messages/{iD}')))

    to_data = json.dumps(mail_data_get.json(), indent=4, sort_keys=True)

    to_data_json = json.loads(to_data)

    email_to = to_data_json['sender']['emailAddress']['address']

    #Grab the email template and shove all of our data into it, and then send_response to send the email.

    with open('email.html') as template_file:
        template = template_file.read().format(headerGrade=headerGrade, toGrade=toGrade, fromGrade=fromGrade, bodyGrade=bodyGrade,
                                                headerGoB=headerGoB, toGoB=toGoB, fromGoB=fromGoB, bodyGoB=bodyGoB, goodOrBad=goodOrBad)

    send_response = send_mail(session=session,
                              subject='Results of your Phishing Email',
                              recipients=email_to.split(';'),
                              body=template)
    print(28*' ' + f'<Response [{send_response.status_code}]>')
    if not send_response.ok:
        pprint.pprint(send_response.json()) # show error message

    #Immediately set up a patch request variable to send to the API to mark the email as read so the loop does not continue to only do one email.

    patchRequest = {'isRead': True}

    isMessageRead = session.patch(api_endpoint(f'me/messages/{iD}'),
                                headers={'Content-Type': 'application/json'},
                                json = patchRequest)

    print('Did Message Patch:',isMessageRead)

    return