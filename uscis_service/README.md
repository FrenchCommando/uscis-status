# USCIS-STATUS

using Beautifulsoup and requests to parse USCIS data

- makes requests to the USCIS website
    - requests are logged and added to the database
        - timestamped (usual datetime format UTC)
        - message is compressed: the number of templates is small
            - `message_stuff.py`
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
- Last updated: Timestamp(pg) / Datetime(python)
- Current Status: "Received / Approved" - specific string
- Current Args: Date - Form Number - Tracking Number
- History: CaseStatus:CurrentArgs|History

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
    - html tags are removed

## User Account

- User with email and password
- Most of the work should already be done in these packages/frameworks
- Mapping User with Watched Cases (some double linked structure?)
- Potentially having fun with middleware and push notifications


# 
I Probably Should Read that

https://codereview.stackexchange.com/questions/155681/optimizing-the-speed-of-a-web-scraper

#

Looks like (for LIN and MSC)
- you can increment the first set fo 5 digits
- then indices go from 50001 to whatever
- Another set: date_start=20900, index_start=10000

#
Read about USCIS number

https://citizenpath.com/uscis-receipt-number-explained/


# Admin exec commands
- Defined in `examples/db_batch.py`
- If using Docker `docker-compose exec uscis_service <COMMAND>`
    - for detached `docker-compose exec -d uscis_service <COMMAND>`
- `COMMAND` is `python -m examples.db_batch <function_name> <function args>`

## Delete cases
- `<function_name>` = `delete`
- `args` = sequence of case numbers

## Refresh Errors
- `<function_name>` = `refresh_errors`
- `args` = None - (they are not externalized)

## Refresh Status
- `<function_name>` = `refresh_status`
- `args` = 
    - status string (leading/trailing space does not work) - Sorry `" Premium Processing Fee Will Be Refunded"`
    - `skip_recent_threshold`: only refresh if current log is older than this number of hours
    - `chunk_size`: 100, for the loop

## Smart Update
- `<function_name>` = `smart_update`
- `args` = 
    - `prefix`: `LIN`, or the other center names
    - `year_start`: `20` (fiscal year 2019-2020  -- starts October 1st)
    - `date_start`: `1` (actual index of day, 1 to something like 326 -> LIN2012350001 - 5 is the separator) 
        - or `0` (if not day number -> LIN 2090000001 - 9 is the separator)  
    - `skip_recent_threshold`: only refresh if current log is older than this number of hours
    - 'chunk_size': '100' - szie of chunks in the loop

## Clear
- `<function_name>` = `clear`
- `args` = None
- Wipes out the data table entirely - use with caution


# Gmail

- `https://developers.google.com/gmail/api/quickstart/python` to generate `credentials.json`
- move `credentials.json` in `gmail` folder
- run `gmail_service.py` to generate authentication token (`token.pickle`)
    - should be in `uscis_service` because this is the cwd of python
- then run docker-compose - token will be copied to the correct path


# Spy on process output
- `htop` to find process PIDs
- 'strace -p1234 -s9999 -e write' where `1234` is the PIDs of the process to spy on
 - `https://unix.stackexchange.com/questions/58550/how-to-view-the-output-of-a-running-process-in-another-bash-session`
