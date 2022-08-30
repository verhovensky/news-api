# News Parser API

Screencast:<br>
[Google drive link](https://drive.google.com/file/d/18TRBeZG2DaC3Tpo5kKoaxIxktu1BfTX6/view?usp=sharing)

#### 1) Create and fill .env file, ensure you have latest docker-compose and Docker installed

.env file example:<br>
```
MYSQL_DATABASE=mysql
MYSQL_USER=mysql
MYSQL_PASSWORD=pa$$word
MYSQL_ROOT_PASSWORD=pa$$word
HOST=mysql

DEBUG=False
```
#### 2) In the root directory execute command:

```
docker-compose up -d
```
#### 3) Execute command to parse and create posts <br> (inside container):
```
docker exec -it <container_id> bash
```
```
python manage.py parse_news docker
```
### Default admin panel credentials:<br>
- username: admin<br>
- password: adminpass<br>
#### Or you can install locally<br>
Ensure you have Python >= 3.8.12
1) python -m venv venv
Make venv
1) source /venv/bin/activate
Activate venv
1) cd djnews && pip install -r requirements.txt
Install required packages
1) edit settings.py to fit your settings (DB, DEBUG, etc.)
Fix your settings
1) python manage.py makemigrations && python manage.py migrate
Make migrations and migrate
1) python manage.py parse_news
Wait for parsing to complete
1) python manage.py runserver
Run server

### API endpoints:

All news:<br>
```
http://127.0.0.1:8000/news/
```
Filter by date:<br>
```
http://127.0.0.1:8000/news/?date__exact=2022-8-25
http://127.0.0.1:8000/news/?date__gt=2022-8-25
http://127.0.0.1:8000/news/?date__lt=2022-8-25
```
Filter by tags:<br>
```
http://127.0.0.1:8000/news/?tags=ozon?
```
Combined filtering:<br>
```
http://127.0.0.1:8000/news/?tags=ozon?date__exact=2022-8-26
```