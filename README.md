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
