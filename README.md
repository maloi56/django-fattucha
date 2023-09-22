# FatTucha - веб-приложение для контроля веса

<h3> Инструкция по сборке проекта:</h3>

#### Build docker

```
sudo docker-compose build
```

#### Start docker

```
sudo docker-compose up
```

#### Build and run in detached mode

```
sudo docker-compose up --build -d
```

#### Stop docker-compose

```
sudo docker-compose down
```
#### Add .env file to src folder 

```
DEBUG=False
SECRET_KEY=<SECRET_KEY>
DOMAIN_NAME=<DOMAIN_NAME>

REDIS_HOST=redis
REDIS_PORT=6379

POSTGRES_DB=<DB_NAME>
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASS>
POSTGRES_HOST=db
POSTGRES_PORT=5432


DB_HOST=db
DB_NAME=<DB_NAME>
DB_USER=<DB_USER>
DB_PASS=<DB_PASS>

EMAIL_HOST=smtp.<SMTP_SERVICE>
EMAIL_PORT=<SMTP_PORT>
EMAIL_HOST_USER=<EMAIL LOGIN>
EMAIL_HOST_PASSWORD=<EMAIL APP PASS>
EMAIL_USE_SSL=True

ACCOUNT_ID=<YOUCASSA_ACC_ID>
KASSA_SECRET_KEY=<YOUCASSA_SECRET_KEY>
```
