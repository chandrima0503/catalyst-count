# Catalyst Count

A Django-based web application for uploading, searching, and managing company data.

<img width="5632" height="2080" alt="image" src="https://github.com/user-attachments/assets/514fd2ac-4bfd-47de-b75e-51e3daa7627d" />


## Features

- User authentication (signup, login, logout)
- Upload company data via CSV (optimized for large files)
- Search and filter companies by multiple fields
- View active users

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your database** in `settings.py`
4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Uploading Large CSV Files

- The upload view supports large CSV files (tested with 100,000+ rows).
- For best performance, the backend uses Django's `bulk_create` in batches.
- Make sure your CSV columns match the expected fields:  
  `name, domain, year founded, industry, size range, locality, country, linkedin url, current employee estimate, total employee estimate`
- Data is parsed and cleaned before saving to the database.

## Notes

- For even faster uploads, PostgreSQL's `COPY` command can be used (see code comments).
- Uploaded files are saved to `MEDIA_ROOT/uploads/`.
- Temporary/processed files are not tracked by git (`.gitignore`).

## License

MIT License



