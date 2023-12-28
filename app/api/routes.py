from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/cars/create', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    car = Car(make, model, year, color)
    db.session.add(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/all', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    cars = Car.query.filter_by().all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/make/<car_make>', methods = ['GET'])
@token_required
def get_cars_by_make(current_user_token,car_make):
    cars = Car.query.filter_by(make = car_make).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/model/<car_model>', methods = ['GET'])
@token_required
def get_cars_by_model(current_user_token,car_model):
    cars = Car.query.filter_by(model = car_model).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/year/<car_year>', methods = ['GET'])
@token_required
def get_cars_by_year(current_user_token,car_year):
    cars = Car.query.filter_by(year = car_year).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/color/<car_color>', methods = ['GET'])
@token_required
def get_cars_by_color(current_user_token,car_color):
    cars = Car.query.filter_by(color = car_color).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<car_id>', methods = ['GET'])
@token_required
def get_car(current_user_token, car_id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        car = Car.query.get(car_id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/cars/<car_id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,car_id):
    car = Car.query.get(car_id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<car_id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, car_id):
    car = Car.query.get(car_id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)