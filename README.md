# RestPlatform
###Quick start:
 1. Create new directory for project
 >$ mkdir ./testAPI
 2. Step into directory
 >$ cd ./testAPI
 3. Create new repository
 >$ git init
 4. Checkout repository
 >$ git clone https://github.com/Shpergl/RestPlatform.git
 5. Install all dependecies from requirements.txt file:
 >$ sudo pip install -r requirements.txt
 6. Migrate DB:
 >$ python manage.py make migrations
 >$ python manage.py make migrate

###To start API tests:
 >$ python manage.py test
###To start API service:
 >$ .python manage.py runserver 0.0.0.0:8000


###In case of using Docker-compose:
 (required: docker==2.0.2, docker-compose==1.10.0)
 1. Build container:
 >$ docker-compose build
 2. Start server:
 >$ docker-compose up
 >$ docker-compose up -d (background mode)

###To start tests use:
 >$ docker-compose run web /usr/local/bin/python manage.py test