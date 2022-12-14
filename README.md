# foodgram-project-react
![example workflow](https://github.com/Ka1las/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg) адрес http://84.201.153.205/recipes
## Описание проекта
Foodgram это ресурс для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате

## Установка проекта локально

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:Ka1las/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
## Запуск проекта в Docker контейнере

Установите Docker

Запустите docker compose:
```
sudo docker-compose up -d --build
```
После сборки появляются 3 контейнера:
 - контейнер базы данных db
 - контейнер приложения backend
 - контейнер web-сервера nginx

Примените миграции:

```
sudo docker-compose exec backend python manage.py migrate
```

Загрузите ингредиенты:

```
sudo docker-compose exec backend python manage.py load_ingrs
```

Создайте администратора:

```
sudo docker-compose exec backend python manage.py createsuperuser
```

Соберите статику:

```
sudo docker-compose exec backend python manage.py collectstatic --noinput
```

### Тестовый суперюзер
Логин: insept@gmail.com
Пароль: Kailas11

## Шаблон наполнения env-файла:

- DB_ENGINE=django.db.backends.<база данных> # указываем, какая база данных
- DB_NAME= <имя> # имя базы данных
- POSTGRES_USER= <логин> # логин для подключения к базе данных
- POSTGRES_PASSWORD= <пароль> # пароль для подключения к БД (установите свой)
- DB_HOST= <сервис> # название сервиса (контейнера)
- DB_PORT= <порт> # порт для подключения к БД 


## Используемые технологии
- asgiref==3.5.0
- backports.zoneinfo==0.2.1
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.12
- coreapi==2.3.3
- coreschema==0.0.4
- cryptography==36.0.1
- defusedxml==0.7.1
- Django==4.0.2
- django-cors-headers==3.11.0
- django-filter==21.1
- django-templated-mail==1.1.1
- djangorestframework==3.13.1
- djangorestframework-simplejwt==4.8.0
- djoser==2.1.0
- drf-extra-fields==3.4.0
- gunicorn==20.1.0
- idna==3.3
- itypes==1.2.0
- Jinja2==3.0.3
- MarkupSafe==2.1.0
- oauthlib==3.2.0
- Pillow==9.0.1
- pkg_resources==0.0.0
- psycopg2-binary==2.8.6
- pycparser==2.21
- PyJWT==2.3.0
- python-dotenv==0.19.2
- python3-openid==3.2.0
- pytz==2021.3
- reportlab==3.6.8
- requests==2.27.1
- requests-oauthlib==1.3.1
- six==1.16.0
- social-auth-app-django==4.0.0
- social-auth-core==4.2.0
- sqlparse==0.4.2
- tzdata==2021.5
- uritemplate==4.1.1
- urllib3==1.26.8