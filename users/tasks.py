from property.models import DetailPropertyAddress
from geopy.geocoders import nominatim
import requests
from time import sleep
from celery import shared_task, task
from django.core.mail import EmailMessage
from subscription.models import Customer
from users.models import User
from propexx.settings.base import PAYSTACK_SECRET_KEY




@task
def create_customer_on_paystack_and_locally(user_id):
    user_query = User.objects.get(id=user_id)
    url = 'https://api.paystack.co/customer'
    payload = {"email": user_query.email,
               "first_name": user_query.first_name,
               "last_name": user_query.last_name,
               "about": user_query.about,
               "phone": user_query.phone_number,
               }
    response = requests.post(url, data=payload,  headers={
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
    data = response.json()
    if data['status']:
        customer = Customer(
            user=user_query, customer_code=data['data']['customer_code'])
        customer.save()


@task
def update_customer_on_paystack_and_locally(user_id):
    user_query = User.objects.get(id=user_id)
    customer_query = Customer.objects.get(user=user_query)
    url = f'https://api.paystack.co/customer/{customer_query.customer_code}'
    payload = {"email": user_query.email,
               "first_name": user_query.first_name,
               "last_name": user_query.last_name,
               "about": user_query.about,
               "phone": user_query.phone_number,
               }
    response = requests.put(url, data=payload,  headers={
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
    data = response.json()


#was passed here because of the conficting behaviour of worker and beat
# @task
# def collect_cleaner_location_details(instance, lat, long):
#     # initialize Nominatim API
#     geolocator = nominatim(user_agent="propexx")
#     location = geolocator.reverse(str(lat)+","+str(long))
#     address = location.raw['address']
#     address = location.raw
#     # traverse the data
#     display_name = address.get('display_name', '')
#     suburb = address.get('suburb', '')
#     adress = address.get('address', '')
#     property_detail = DetailPropertyAddress.objects.get_or_create(
#         property = instance,
#         address = adress,
#         display_name = display_name
    # )
 
 

