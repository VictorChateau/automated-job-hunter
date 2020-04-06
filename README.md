# automated-job-hunter
Searching and applying for jobs can be repetitive and takes a lot of time... so I made a script to do it for me!

Scrum_log.pdf describes my use of Scrum during the project, including the initial sprint plan, the product backlog and daily scrums.

All files are required in order to run the script except for Scrum_log.pdf and this README. Aditionally, you will need to have selenium + a web driver for chrome + chrome itself. See https://selenium-python.readthedocs.io/installation.html for help installing selenium. You will also need to have at least one resume uploaded on SEEK and you will need to enter a valid SEEK username and password into user_details.txt (The username must be on the first line of the file and the password must be on the second line). links_for_manual_application.txt contains links from job ads which redirected the web driver away from the SEEK website.

Note that this script may no longer work if SEEK has significantly modified the layout of their website, but feel free to fork this project and create an updated version.
