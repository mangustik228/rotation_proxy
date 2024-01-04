## Запуск и создания нужных бд `db_postgres`: 

```bash 

# Запуск контейнера 
docker compose up --build -d db_postgres

# Заходим в postgres 
docker compose exec db_postgres psql -U postgres

# Создаем бд  
CREATE DATABASE proxies;
CREATE DATABASE test_proxies;

```

## Запуск `redis`

```bash 

# Запуск 
docker compose up --build -d db_redis 

``` 

## Запуск сервиса `web_prod` 

```bash 
docker compose up --build -d web_prod 
``` 

## Пример файла `.env`: 
```bash 
PYTHONPATH=:app
MODE=PROD
APIKEY=SECRET_API_KEY

POSTGRES_DB=proxies
POSTGRES_PASSWORD=SECRET_POSTGRES_PASSWORD
POSTGRES_USER=postgres
POSTGRES_HOST=db_postgres
POSTGRES_PORT=5432

TEST_POSTGRES_DB=test_proxies
TEST_POSTGRES_PASSWORD=SECRET_POSTGRES_PASSWORD
TEST_POSTGRES_USER=postgres
TEST_POSTGRES_HOST=db_postgres
TEST_POSTGRES_PORT=5432

DEV_POSTGRES_DB=dev_proxies
DEV_POSTGRES_PASSWORD=SECRET_POSTGRES_PASSWORD
DEV_POSTGRES_USER=postgres
DEV_POSTGRES_HOST=db_postgres
DEV_POSTGRES_PORT=5432

REDIS_PASSWORD=SECRET_REDIS_PASSWORD

```



## Пример файла `.env.db`: 


```bash 

POSTGRES_USER=postgres
POSTGRES_PASSWORD=SECRET_POSTGRES_PASSWORD
REDIS_PASSWORD=SECRET_REDIS_PASSWORD
PGADMIN_DEFAULT_PASSWORD=NOT_SUPER_SECRET # Только если нужен pgadmin
PGADMIN_DEFAULT_EMAIL=example@gmail.com # Только если нужен pgadmin

```