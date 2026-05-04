Welcome to Harmony
This project was created collaboratively among the three software engineering students: Dani Dimovski, Giovanni Clerici, Jerry Gutierrez.

Please ensure python 3.10 or higher is installed prior to continuing
You can download python from python.org/downloads, this provides you with the python installer for your computer

Firstly, To run “Harmony” locally the user needs to ensure they create and activate a virtual environment by doing the following commands on the terminal:
python -m venv venv
venv\Scripts\activate

For the rest of the software, you can navigate to the project root folder and install all the required dependencies by simply copying and pasting the following commands in the Command Prompt: 

pip install -r requirements.txt

this will install the following dependencies:
asgiref
Django
sqlparse
tzdata
pillow


Once these steps have been completed, open the project folder in the terminal or manually change directory to myproject.
You can do so by opening the terminal and typing the following command:
cd myproject
Once the project folder is opened in the terminal run the following codes:
python manage.py migrate
python manage.py runserver

At this point the application is running, some output will appear. To access the home page, find the IP address (http://127.0.0.1:8000/) and ctrl+click it. This will open a new browser
Now you can create an account, log in and access the system services



Sample terminal output:
Django version 6.0.3, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.


Side Note: Creating a Superuser
If you want to create an admin you have to type in the following command from the myproject folder:
python manage.py createsuperuser

From here you need to log in the admin to grant regular users admin privileges:
http://127.0.0.1:8000/admin
Once isAdmin is set, that user can also access the in-app Create Superuser page at:
   http://127.0.0.1:8000/create_superuser/