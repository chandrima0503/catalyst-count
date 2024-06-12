# catalyst-count
Django assignment for Catalyst

Follow these steps to run the app.

1.Clone the repository 

2. Unzip the repo and navigate to cd catalyst-count
   
3. python -m venv venv
   
4. source venv/bin/activate for mac OR venv\Scripts\activate for windows

5. run pip install -r requirements.txt

6. update the .env with your credentials for database url and secret key.
   DATABASE_URL=postgres://username:password@localhost:5432/catalyst_count

7. generate a SECRET_KEY=""


8. Set up the database : python manage.py migrate

9. Start the development server : python manage.py runserver

10. Register a new account and login

11. Once logged in, navigate to the Upload Data section.

12. Click on the "Upload Data Tab" button and select a CSV file to upload.

13. After the file is uploaded, perform the desired operations on the data.



