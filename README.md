Hello This A Laywer system With Django MVT to manage the cases and analys case data

this system give You a  control to create 

1 - Home Page

2 - Clients
  + Cases and every case you can add to it 
    - session (add date session and the session order)
    - Files
    - Case Payment (Payment By date and total)
    - Add Events (Start Date And End Data And The Task)
    
3 - a page to calculate the next Sessions in 30 days

4 - a page to show Events per day and pick it from a calendar and create a dynamic pdf for the events that in this day

5 - A Dashboard
  + Contreol
    - Home Page Show
    - Users (Control and Give Permissions To Users)
    - Cases (Control and see Cases analysis With Charts )
    - Sales ( analysis sales Per monthe With Charts )
    
6 - 3 Permissions Level (assistant - lawyer - Super User)

7 - 2 Languages (Arabic - English)

8 - authentication and registration system

Installation
- create an py venv
- pip install -r requirments.txt
- py manage.py makemigrations
- py manage.py migrate
- py manage.py runserver


