__author__ = 'kobyn'

from celery import Celery

celery = Celery('cosmo.celery',
                broker='amqp://',
                backend='amqp://')
