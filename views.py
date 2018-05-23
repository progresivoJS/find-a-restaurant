from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[i.serialize for i in restaurants])
    elif request.method == 'POST':
        location = request.args.get('location')
        mealType = request.args.get('mealType')
        restaurant = findARestaurant(mealType, location)

        if restaurant != 'No Restaurants Found':
            newItem = Restaurant(
                restaurant_name = restaurant['name'], restaurant_address = restaurant['address'], restaurant_image = restaurant['image'])
            session.add(newItem)
            session.commit()
            return jsonify(restaurant=newItem.serialize)


@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    pass


if __name__ == '__main__':
    app.debug = True
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000)