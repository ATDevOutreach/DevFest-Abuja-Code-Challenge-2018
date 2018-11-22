# Pusher [Deployed version](https://puzher.herokuapp.com)

## Configurations
Configure Database Settings in ~/.bashrc file:
    - Add the following lines to the end of the file and run `source ~/.bashrc`
    - `export MY_EMAIL_HOST_USER=YourEmail@gmail.com`
    - `export MY_EMAIL_HOST_PASSWORD=YourPassword`

Windows Users:
    - `set MY_EMAIL_HOST_USER=YourEmail@gmail.com`
    - `set MY_EMAIL_HOST_PASSWORD=YourPassword`

## Setup
- Clone the repo and checkout to the branch: `git checkout 2348136457976`
- Install dependencies: `pip install -r requirements.txt`
- Migrate database: `python manage.py migrate`
- Create super user: `python manage.py createsuperuser`
- Run server: `python manage.py runserver`
