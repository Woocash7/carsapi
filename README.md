### carsAPI

## Runing dev server and sqlite3 db

- Install python3
- (Optional) Run virtualenv
    - Install virtualenv package `pip install virtualenv`
    - Create virtualenv `virtualenv venv`
    - Activate virtualenv:
        - Windows `venv/scripts/activate`
        - Linux `source venv/bin/activate`
- Clone this repository `git clone https://github.com/Woocash7/carsapi.git` 
- Change dir to carsapi project directory `cd carsapi`
- Install dependencies from requirements.txt `pip install -r requirements.txt`
- Migrate `python manage.py migrate --settings=carsapi.settings.dev`
- (Optional) Load fixtures `python manage.py loaddata test_fixtures.yaml --settings=carsapi.settings.dev`
    > Super user -> email: `admin@test.com` , password: `test`
- Run tests `python manage.py test --settings=carsapi.settings.dev`
- Run dev server `python manage.py runserver --settings=carsapi.settings.dev`

## Running with docker

- Install docker
- Build selected docker container `docker-compose -f docker-compose.yaml up -d --build`
- Run selected docker container `docker-compose -f docker-compose.yml up -d`