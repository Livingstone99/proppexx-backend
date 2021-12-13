from users.utils import cancel_paystack_subscription
from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@periodic_task(
    # cronjobs checks condition midnight everyday
    # run_every = (crontab(minute=0, hour='0, 3, 6')),
    run_every = (crontab()),
    name = "cancel subscription",
    ignore_result = True
)    
def cancel_susbscription():
    # cancel_paystack_subscription()
    logger.info('auto cancellation cron job deactivated')