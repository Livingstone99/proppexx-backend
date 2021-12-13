import os
from users.utils import delete_draft

from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


if os.getenv('SETTINGS_MODULE_PATH') == 'propexx.settings.local':
    logger = get_task_logger(__name__)

    # """
    # to switch cronjob scehduler from every minute to midnight or every 15 minutes"""
    # cronjob = os.getenv('CRONJOB')
    # if cronjob == 'every_minute':
    #     cron_timer = crontab()
    # elif crontab == 'midnight':
    #     cron_timer = crontab(minute=0, hour=0)
    # elif crontab == '15 minutes':
    #     cron_timer = crontab(minute='*/15')
    @periodic_task(
        # cronjobs checks condition midnight everyday
        run_every = (crontab(minute=0, hour=0)),
        name = "delete_overdue_drafted_property",
        ignore_result = True
    )    
    def task_delete_overdue_drafted_property():
        delete_draft()
        logger.info('draft property successfully delete')
else:
    logger = get_task_logger(__name__)

    @periodic_task(
        # cronjobs checks condition midnight everyday
        run_every = (crontab(minute=0, hour=0)),
        name = "delete_overdue_drafted_property",
        ignore_result = True
    )    
    def task_delete_overdue_drafted_property():
        delete_draft()
        logger.info('draft property successfully delete')

