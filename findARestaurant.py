from geocode import getGeocodeLocation
import json
import requests
import httplib2

import sys
import codecs

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "SBIOLOMVSZBL0LYSFSEHB10TR12I1IWCVP1ZRMLUBXBSBSCT"
foursquare_client_secret = "3YCRR5ZWROSX1EOI2IB2C0DE25OYR5V2HSQXHULZH44UH3HW"


def findARestaurant(mealType, location):
    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    latitude, longitude = getGeocodeLocation(location)

    # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    # HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&query={}&v=20180522'.format(
        foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType)

    h = httplib2.Http()
    response, content = h.request(url)
    result = json.loads(content)

    if result['response']['venues']:
        # 3. Grab the first restaurant
        first_restaurant = result.get('response').get('venues')[0]

        # 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture

        url = 'https://api.foursquare.com/v2/venues/{}/photos?client_id={}&client_secret={}&v=20180522'.format(first_restaurant.get('id'),foursquare_client_id, foursquare_client_secret)
        result = json.loads(h.request(url)[1])
        # 5. Grab the first image
        if result['response']['photos']['items']:
            first_picture = result['response']['photos']['items'][0]
            prefix = first_picture['prefix']
            suffix = first_picture['suffix']
            imageURL = prefix + "300x300" + suffix
        # 6. If no image is available, insert default a image url
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

        # 7. Return a dictionary containing the restaurant name, address, and image url
        restaurant_info = {
            'name': first_restaurant['name'],
            'address': first_restaurant['location']['formattedAddress'],
            'image': imageURL
        }

        restaurant_name = restaurant_info['name']
        restaurant_address = ""
        for i in restaurant_info['address']:
            restaurant_address += i + " "

        print("Restaurant name : {}".format(restaurant_name))
        print("Restaurant address : {}".format(restaurant_address))
        print("Image : {}".format(restaurant_info['image']))
        return restaurant_info
    else:
        print("No restaurants for {}".format(location))
        return "No restaurants found"


if __name__ == '__main__':
    findARestaurant("Pizza", "Busan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
