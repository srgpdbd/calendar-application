# Install
```
git clone https://github.com/srgpdbd/calendar-application.git
pipenv shell
pipenv install

rename calendar_application/__settings_local.py to settings_local.py

provide database settings in settings_local.py

python manage.py migrate
```
# Run dev server

```
python manage.py runserver
```

# Run tests 
```
coverage run manage.py test
coverage report
```
