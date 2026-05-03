Welcome to Harmony
This project was created collaboratively among the three software engineering students: Dani Dimovski, Giovanni Clerici, Jerry Guiterrez.
To run “Harmony” locally the user needs to ensure that they have installed on their computer the following software: “Python”, “Django”, and “Pillow”.
You can download python from python.org/downloads, this provides you with the python installer for your commputer
For the rest of the software you can install it by simply copying and pasting the following commands in the Command Prompt: 
* pip install django
* pip install pillow
Once these steps have been completed, the user can run the program. To do so, open the project folder in the terminal or manually change directory to the one of the project folder.
You can do so by opening the cmd and typing the following command:
cd “C:\folder address”.
Once the project folder is opened in the terminal digit the following:
python manage.py runserver
At this point the application is running, a bunch of writings will be showed in the terminal, and to access the home page, you must find the IP address and ctrl+click it.
Now you can create an account, log in and access the system services








Sample terminal output:
Instruction:
Ctrl+click the highlighted IP


Output:
Django version 6.0.3, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.






Side Note:
If you want to create an admin you have to type in the following command once the right directory is opened:
python manage.py createsuperuser
From here you need to log in the admin part of the website, to grant regular users admin privileges. This can be done at the following
http://127.0.0.1:8000/admin
