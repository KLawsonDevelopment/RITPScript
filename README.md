### KLawsonDevelopemnt Phishing Script
Good morning, good afternoon, good evening! This is a script I developed for Rocket IT for the sole purpose of brute forcing against possible phishing emails.

# Languages
Exclusively Python based, outside of an HTML response layout.

# Methodology
The plan was to take any emails received to an Outlook email, run the entire script against it, and shoot back a response that was able to tell a user 'Yes, do open this' or 'No, do not open this'. We do that by:

1) Checking for unread emails
2) Ripping out the Header, To, From, and Body of the email
3) Run several checks such as: is it from a domain we know? Are there nam10safelinks? Is it a gmail/hotmail/yahoo? To determine if the email is safe or not.
4) Update over time to be less brute force and more finesse based, such as reaching out to different APIs to see if the email is from a safe location in the world or if the domain used is already a bad link.

# Version 1 Plans
This script is very much in a prototype phase. If I am able to do a Version 1 of this program, it would include:
API Checks against he domain
API Checks against known bad links, and putting them into a text file to reference later
A faster system that doesn't need to use time.sleep to function
Running 24/7 without any loop breaks
A GUI so that I can see exactly what it is doing (Javascript possibly)
A way to alert me if the script crashes or goes offline

