from geopy.geocoders import Nominatim


def collect_cleaner_location_details(prop_id, lat, long):
    # initialize Nominatim API
    geolocator = Nominatim(user_agent="propexx")
    location = geolocator.reverse(str(lat)+","+str(long))
    address = location.raw['address']
    address = location.raw
    # traverse the data
    display_name = address.get('display_name', '')
    suburb = address.get('suburb', '')
    adress = address.get('address', '')
  
    print(address)
    print('name : ', display_name)
    print('Address :',adress )
 
collect_cleaner_location_details(2, 8.9384760000000000, 7.5446446000000000)