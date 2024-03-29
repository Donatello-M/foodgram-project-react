![example workflow](https://github.com/Donatello-M/foodgram-project-react/actions/workflows/main.yml/badge.svg)

**Доступ к админке**
login/password: donatello/32282
# [Продуктовый помощник](http://51.250.101.97/)

**Foodgram** - это сервис, позволяющий создавать и делиться своми уникальными рецептами и подписываться на таких же умелых кулинаров, как Вы. 

Рецепты можно сохранять в избранные, чтобы не забыть: чем накрыть праздничный стол. А также сохранять и выгружать из "Корзины", чтобы при приходе из магазина не оказалось недостающих ингредиетов.

## Запуск проекта на локальной машине
### Склонировать репозиторий на локальную машину:
```
git clone https://github.com/Donatello-M/foodgram-project-react.git
```
### Подготовка и запуск:
1) Создайте файл окружения <./backend/.env> с параметрами:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<Название бд>
POSTGRES_USER=<Логин привелегированного пользователя в бд>
POSTGRES_PASSWORD=<Пароль привелегированного пользователя в бд>
DB_HOST=db
DB_PORT=5432
DJANGO_KEY=<Django SECRET_KEY>
```  
2) Установите Docker, docker-compose:
[Это можно сделать с помощью документации](https://docs.docker.com/engine/install/)
3) Не забудьте отключить локальный nginx и postgresql, если что-то включено:
```
sudo killall nginx
sudo systemctl stop postgresql
```
4) Соберите docker-compose из директории ./infra/:
```
sudo docker-compose up -d --build
```
5) После успешной сборки должны образоваться **3** контейнера. frontend быстро своё отработает и сляжет, на него внимание не обращаем. Перейдем в контейнер backend:
- Посмотреть контейнеры:
```
sudo docker ps
```
- Перейти в контейнер
```
sudo docker exec -it <Название контейнера backend> bash
```
6) Теперь проделаем работу со статикой и миграциями в контейнере backend:
- Соберем статику:
```
python manage.py collectstatic
```
- Миграции
```
python manage.py migrate
```
7) ГОТОВО! Теперь можно перейти по адресу <http://localhost> и проверить работоспособность приложения.
## Документация 
Увидеть спецификацию API вы сможете по адресу <http://localhost/api/docs/>

> **Технологии**
- Django🙃
- Django REST Framework🥵
- Docker🐋
- GitHub Actions
- PyCharm🥴
- vim🥲
- MacOS
- nginx
- PostgreSQL🐘
- Python3.7🐍
