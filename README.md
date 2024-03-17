Разработка LMS-системы, в которой каждый желающий может размещать свои полезные материалы или курсы.
 
Установите все зависимости из файла requirements.txt
Создайте файл **.env** и заполните его по образцу из **.env.sample**


Для наполнения БД тестовыми данными необходимо выполнить команды:
**python manage.py groups** - создания групп пользователей для разграничения прав
**python manage.py ctu** - создания тестового пользователя
**python manage.py test_db** - создание курсов и уроков
**python manage.py payment** - добавление платежей пользователю

Для запуска проекта с планировщиком заданий выполните команды:
**python manage.py runserver**
**celery -A config worker -l INFO** (в случае запуска под ОС Windows **celery -A config worker -l INFO -P eventlet**)
**celery -A config beat -l INFO -S django**