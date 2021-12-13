# from users.tasks import collect_cleaner_location_details
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AssignPropertyToDeveloper, Property


# @receiver(post_save, sender = Property)
# def cleaner_prop_details_collection(sender, instance, created, *args, **kwargs):
#     if created:
#         collect_cleaner_location_details.delay(instance.id, instance.latitude, instance.longitude)
#         print('done .....')
@receiver(post_save,  sender = Property)
def create_member_instance(sender, instance, created,*args,**kwargs ):
    if created:
        if instance.agent.user_type == 'developer':
            AssignPropertyToDeveloper.objects.get_or_create(property = instance, developer = instance.agent)
            

