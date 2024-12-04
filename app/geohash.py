import requests
import geohash2
from app.geoapify import GEOAPIFY_KEY

def address_sanity_check(input_text):

    address_to_coord_url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text":input_text,
        "apiKey": GEOAPIFY_KEY,
        "lang":'en',
        "limit":1,
        "format":'json',
    }
    
    # Send the GET request
    response = requests.get(address_to_coord_url, params=params)

    if response.status_code == 200:
        result = response.json()
        
        result = result['results'][0] # we only have one result, remove the outer result layer
        result_type = result['result_type'] #[unknown, amenity, building, street, suburb, district, postcode, city, county, state, country].        
        
        match result_type:
            case 'amenity':
                # this is a business name or non-address (Ex. Georgetown University)

                # each type will have this sanity_check which is a dumbed down version of the result that is shown to the user for validation
                sanity_check = {
                    'Result Type':'Business or Non-Address Location',
                    'Name':result['name'],
                    'Address Line 1':result['address_line1'],
                    'Address Line 2':result['address_line2'],
                }
            
            case 'building':
                # this is a street address (Ex. 3700 O St NW)
                sanity_check = {
                    'Result Type':'Address',
                    'Address Line 1':result['address_line1'],
                    'Address Line 2':result['address_line2'],
                }
            
            case 'street' | 'postcode' | 'city' | 'country':
                # this is a literal street, postcode, city, or country (Ex. O St. NW)
                sanity_check = {
                    'Result Type':result_type.capitalize(),
                    'Address Line 1':result['address_line1'],
                    'Address Line 2':result['address_line2'],
                }

            case 'state' | 'country':
                # throw an error here for more specificity, states or countries are too broad
                print('ERR')

            case 'suburb' | 'district':
                # throw an error here, is it worth supporting? 
                print('ERR')

        # still have to cut the len to support ticketmaster api
        geohash_code = geohash2.encode(result["lat"], result["lon"])    
        return sanity_check, geohash_code
    
    else:
        print('ERR')

if __name__ == "__main__":
    destination = input('Where Are You Traveling? ')
    sanity_check, geohash = address_sanity_check(destination)
    for key, value in sanity_check.items():
        print(f'{key}: {value}')
    
    print(geohash)