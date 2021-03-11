# Foodgram-project

Foodgram-project - social network for people, passionate about cooking! It is like Instagram, but only for tasty recipes :) 

## Getting Started

To start this project you need to clone this repository to your local machine. 

### Prerequisites

After cloning the repo you need to install all the requirements with the command below. 

```
pip install -r requirements.txt
```
You also need Docker to be installed and started. Please check [docker.com](https://www.docker.com) for further instructions. 

### How to use

To start the app you need only one simple command. Check if you are in the root directory of the project.

```
docker-compose up
```

It will start the containers and project will be available on http://0.0.0.0:80/home/
Admin interface may be found at http://0.0.0.0:80/admin/

You need to collect static with the command 

```
docker-compose exec web python manage.py collectstatic
```

To create superuser use command below

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser 
```

To fill database with test data use the command 

```
docker-compose exec web python manage.py loaddata ing.json
```

You may also add all necessary information (as tags and recipes) via admin interface. 

## Authors

* **Nika Dmitrievskaya** - *Initial work* - [kabanovanika](https://github.com/kabanovanika) - Yandex.Praktikum student 🤓 
