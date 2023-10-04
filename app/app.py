#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
# dburi = 'postgres://paxful_login_user:vWseP9sNrGRMsqCnDyiMErVC5OcP5LLg@dpg-ckceqh6smu8c73cb0eng-a.oregon-postgres.render.com/paxful_login'
# app.config['SQLALCHEMY_DATABASE_URI'] = configx(dburi)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return {
        'message': 'Welcome to SuperHeroes'
    }, 200


@app.route('/powers', methods=['GET'])
def get_powers():
    powers_list = Power.query.all()
    if powers_list:
        return jsonify([power.as_dict() for power in powers_list]), 200
    else:
        return jsonify({'error': 'Power not found'}), 404


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.as_dict()), 200
    else:
        return jsonify({'error': 'Power not found'}), 404


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        power.description = data['description']

    db.session.commit()
    return jsonify(power.as_dict()), 200


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes_list = Hero.query.all()
    if heroes_list:
        return jsonify([{'id': her.id, 'name': her.name, 'super_name': her.super_name} for her in heroes_list]), 200
    else:
        return jsonify({'error': 'No Hero found'})


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        power_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.heropowers]
        }
        return jsonify(power_data), 200
    else:
        return jsonify({'error': 'Hero Not Found'}), 404


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')
    
    if not hero_id or not power_id or not strength:
        return jsonify({'errors': ["Validation Errors"]})
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'error': 'Hero or Power not found'}), 404

    hero_power = HeroPower(hero_id=hero, power_id=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero.as_dict()), 200


@app.route('/heroes', methods=['POST'])
def create_hero():
    data = request.get_json()
    name = data.get('name')
    super_name = data.get('super_name')

    if not name or not super_name:
        return jsonify({'error': ['Validation Errors']}), 400

    hero = Hero(name=name, super_name=super_name)
    db.session.add(hero)
    db.session.commit()

    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}), 201


@app.route('/powers', methods=['POST'])
def create_power():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Validation error'})

    power = Power(name=name, description=description)
    db.session.add(power)
    db.session.commit()

    return jsonify({'id': power.id, 'name': power.name, 'description': power.description}), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
