#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return {
        'message': 'Welcome to SuperHeroes'
    }, 200


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes_list = Hero.query.all()
    if heroes_list:
        return jsonify([{'id': h.id, 'name': h.name, 'super_name': h.super_name} for h in heroes_list]), 200
    else:
        return jsonify({'error': 'Heroes not found'})


@app.route('/powers', methods=['GET'])
def get_powers():
    powers_list = Power.query.all()
    if powers_list:
        return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in powers_list]), 200
    else:
        return jsonify({'error': 'Power not found'})
    


if __name__ == '__main__':
    app.run(port=5555)
