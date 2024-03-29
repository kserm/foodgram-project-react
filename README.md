# Дипломный проект "Foodgram" на учебном курсе Python-разработчик от Яндекс.Практикум.
##### студент: Ермачков Константин
![foodgram workflow](https://github.com/kserm/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
____________________________________________
## **Адрес проекта.**
### [foodgram-eks.ddns.net](http://foodgram-eks.ddns.net/)

### Учетная запись администратора:
- e-mail: admin_user1@example.com
- password: adpass123 

____________________________________________
## **Описание.**
Проект Foodgram «Продуктовый помощник» представляет собой онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## **Используемые технологии.**
- Python 3.7
- Django 3.2
- PostgreSQL 13
- DRF
- Djoser
- Nginx
- Gunicorn
- Docker

## **Шаблон наполнения env-файла.**
- ``` DB_ENGINE=django.db.backends.postgresql```
- ```DB_NAME=postgres```
- ```POSTGRES_USER=postgres```
- ```POSTGRES_PASSWORD=postgres```
- ```DB_HOST=db```
- ```DB_PORT=5432```

## **Описание команд для запуска проекта локально.**
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:kserm/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
cd backend/foodgram
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
python3 manage.py runserver 80
```

### **Создание суперпользователя**
Для создания superuser выполните команду:
```
python3 manage.py createsuperuser
```
### **Описание команды для заполнения базы данными.**
После выполнения миграций:
```
python3 manage.py loaddata fixtures.json
```

### **Для подключения frontend**
Перейти в директорию:
```
 cd ../../infra
```
Выполнить команду:
```
docker-compose up
```

## **Описание команд для запуска приложения в контейнерах.**
Перейдите в раздел infra/ и выполните команду:
```
docker-compose up -d --build
```

Выполните миграции:
```
sudo docker-compose exec backend python manage.py migrate
```

Для создания superuser выполните команду:
```
sudo docker-compose exec backend python manage.py createsuperuser
```

Для сбора статики выполните команду:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

## **Примеры запросов**

Примеры запросов и варинты ответов доступны после запуска сервера по адрессу:

При запуске локально:
http://localhost/api/docs/

При работе с удаленным сервером:
http://foodgram-eks.hopto.org/api/docs/
