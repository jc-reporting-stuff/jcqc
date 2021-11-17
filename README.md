# Oligos and Sequencing Website

## Installation

1. Clone repo into new directory.
2. Create a new virtual environment in the new directory: `python -m venv venv`.
3. Activate virtual environment: `source venv/bin/activate` (linux) `venv\Scripts\activate` (windows).
4. Load required packages: `pip install -r requirements/<env>.txt` (look in requirements folder for <env> options).
5. Start server: `python manage.py runserver --settings=core.settings.<env>` (look in core/settings for <env> options).

## Database

Currently set up to use POSTGreSQL. Will need to create a 'secrets' file as in core/settings/base.py in order
to provide ports and credentials.
