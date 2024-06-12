# catalyst-count
Django assignment for Catalyst

Follow these steps to run the app.

1.Clone the repository 

2. Unzip the repo and navigate to cd catalyst-count
   
3. python -m venv venv
   
4. source venv/bin/activate for mac OR venv\Scripts\activate for windows

5. run pip install -r requirements.txt

6. Set up the database : python manage.py migrate

7. Start the development server : python manage.py runserver

8. Open the project's settings file: csv_uploader/settings.py. Locate the INSTALLED_APPS section and ensure that the following apps are included: INSTALLED_APPS = ['allauth','allauth.account']

9. Set up the authentication backend: AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend','allauth.account.auth_backends.AuthenticationBackend']

10. Register a new account and login

11. Once logged in, navigate to the Upload Data section.

12. Click on the "Upload Data Tab" button and select a CSV file to upload.

13. After the file is uploaded, perform the desired operations on the data.



