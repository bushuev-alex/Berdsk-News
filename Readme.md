# Launch 
1. activate venv
2. install from requirements.txt
3. cd berdsk_news
4. python manage.py runserver  (Django)

## Scrapyd server
1. cd berdsk_news/parser
2. scrapyd
3. curl http://localhost:6800/daemonstatus.json
4. curl http://localhost:6800/schedule.json -d project=parser -d spider=ksonline

## Celery schedule spiders
1. cd berdsk_news
2. celery -A celery_tasks worker -l INFO -B