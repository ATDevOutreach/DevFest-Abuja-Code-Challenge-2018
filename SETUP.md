# Pusher

## Configurations
Configure Database Settings in ~/.bashrc file:
    - Add the following lines to the end of the file and run `source ~/.bashrc`
    - `export MY_EMAIL_HOST_USER='YourEmail@gmail.com'`
    - `export MY_EMAIL_HOST_PASSWORD='YourPassword'`

## Setup
- Clone the repo and change to project directory: `cd pusher`
- Install dependencies: `pip install -r requirements.txt`
- Migrate database: `python manage.py migrate`
- Create super user: `python manage.py createsuperuser`
- Run server: `python manage.py runserver`
