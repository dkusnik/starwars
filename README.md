# starwars

Create a virtualenv
the CSV files in `CSV_STORAGE_DIR`
`python -m venv`

Activate it
`. .ve/bin/activate`

Install necessary packages:
`pip install -r requirements.in`

Set up `SWAPI_API_URL` in `starwars/settings.py` additionally you can also set up the dir where to save 
the CSV files in `CSV_STORAGE_DIR`
Run the server:
`python manage.py runserver 0.0.0.0:8000`


