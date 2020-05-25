USCIS-STATUS

using Beautifulsoup and mechanize to parse the website of USCIS

- makes requests to the USCIS website
    - requests are logged and added to the database
        - timestamped (usual datetime format with ms)
        - message is compressed: the number of templates is small
            - classes (can they be automatically generated from)
    - this is the only way to add entries to the database
- request to the api
    - managed by api
        - prioritize simple requests to database
        - scarce requests to website directly
- periodic (daily) call to the website
    - feed database with pending cases data
    - list of pending cases to be managed
- user account to manage subscription to cases
- email service to send subscription results
- api for useful statistics
- website
- android app


# Databases

## Case data

- Case Number
- Last updated: Timestamp ? String ?
- Current Status: Date - Case Status(kwargs)
- History: Date:CaseStatus(kwargs)|History

## Status

- Fancy (too fancy) mapping from status type to message content
- Using a DB hoping that the code can automatically add new types as the code runs

`Case Received -> "Your case {case_number} has been accepted"`

Need to check if same title always lead to same content

- Should be able to rebuilt the initial message by using the Case Status String
    - Case Number is an (the first) argument
    - Date (not last updated) is another argument
    - Other args are, for example, 
        - another date (deadline for receipt)
        - form number and name
        - tracking number

## User Account

- User with email and password
- Most of the work should already be done in these packages/frameworks
- Mapping User with Watched Cases (some double linked structure?)
- Potentially having fun with middleware and push notifications


# 
I Probably Should Read that

https://codereview.stackexchange.com/questions/155681/optimizing-the-speed-of-a-web-scraper

#
Read about USCIS number

https://citizenpath.com/uscis-receipt-number-explained/