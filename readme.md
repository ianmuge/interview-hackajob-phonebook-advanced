# Hackajob Phonebook Advanced 
## Dependecies
The solution is built using flask on Python 3.7.3
Other pertinent dependencies are listed in the requirements file
## Run instructions
- Go to project root
- Install dependencies 
    ```
    pip install -r requirements.txt
    ```
- Set Flask run variables\
    On windows:\
    CMD:
    ```
    set FLASK_APP=app.py
    ```
    Powershell
    ```
    $env:FLASK_APP = "app.py"
    ```
    On *nix:
    ```
    export FLASK_APP=app.py
    ```
- Start the service
    ```
    python -m flask run
    ```
- The UI should be available on: http://127.0.0.1:5000
## To reinitialze the sqlite3 database
- In the ``app.py`` file, set the init variable to ``True`` and restart the application.
- The application will fetch the data from the remote endpoint and recreate the database and table upon making the first web request.
*The shipped sqlite db has the default 10 records, pre-fetched from the remote endpoint*
   

