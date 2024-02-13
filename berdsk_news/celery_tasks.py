from celery import Celery, shared_task
from celery.schedules import crontab
from parser.celery_funcs import launch_spider

# clry_tknzr = Celery("tokenizer", broker="redis://127.0.0.1:6379")
clry_spdr = Celery("parser", broker="redis://127.0.0.1:6379")

# clry_tknzr.conf.beat_schedule = {'tokenize_ml_keywords_60m': {'task': 'tokenizer.tokenize_from_db.main',
#                                                               'schedule': 60 * 60,
#                                                               'args': ("temp_article",),
#                                                               },
#                                  }

clry_spdr.conf.beat_schedule = {'launch_berdskbn_45m': {'task': 'parser.celery_funcs.launch_spider',
                                                        'schedule': crontab(minute="*/45", hour="*/1"),
                                                        'args': ("berdsk-bn.ru",),  #
                                                        },
                                'launch_ksonline_45m': {'task': 'parser.celery_funcs.launch_spider',
                                                        'schedule': crontab(minute="*/45", hour="*/1"),
                                                        'args': ("ksonline.ru",),  #
                                                        },
                                'launch_ngs_15m': {'task': 'parser.celery_funcs.launch_spider',
                                                   'schedule': crontab(minute="*/15", hour="*/1"),
                                                   'args': ("ngs.ru",),  #
                                                   },
                                'launch_sibfm_15m': {'task': 'parser.celery_funcs.launch_spider',
                                                     'schedule': crontab(minute="*/15", hour="*/1"),
                                                     'args': ("sib.fm",),  #
                                                     },
                                'launch_acadinfo_90m': {'task': 'parser.celery_funcs.launch_spider',
                                                        'schedule': crontab(minute="*/30", hour="*/2"),
                                                        'args': ("academ.info",),  #
                                                        },
                                }
