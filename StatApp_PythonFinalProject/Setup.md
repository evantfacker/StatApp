#ALERT: you will likly need to delete the "env" folder, after deleting "env" please run the insturction below after you cd into the in the "StatApp_PythonFinalProject"

# Create a new virtual environment called "env"
python -m venv env

# Active your virtual environment (so an Python commands are run in the virtual envrionment)
env/Scripts/activate.bat //In CMD
env/Scripts/Activate.ps1 //In Powershell
source env/bin/activate // On mac

# if you get an error about not being able to run scripts on this system (when using Powershell), open powershell as an administrator and run this:
Set-ExecutionPolicy RemoteSigned

# Once in your virtual environment, install all your packages you need
pip install -r requirements.txt
 
# If you install new packages run this:
 pip freeze > requirements.txt

# If MacOS, you may need to run these seperately 
pip install scikit-learn
pip install django
pip install django_pandas


 # To run the project from parent folder "StatApp" follow the instructions below:
 cd StatApp_PythonFinalProject
 cd statapp
 python manage.py runserver
 
 
