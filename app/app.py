#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
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


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes_list = Hero.query.all()
    if heroes_list:
        return jsonify([hero.as_dict() for hero in heroes_list]), 200
    else:
        return jsonify({'error': 'Hero not found'}), 404


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.as_dict()), 200
    else:
        return jsonify({'error': 'Hero not found'}), 404


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


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'error': 'Hero or Power not found'}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero.as_dict()), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
