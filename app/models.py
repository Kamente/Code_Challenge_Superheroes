from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    powers = db.relationship('HeroPower', backref='hero', lazy=True)


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    heroes = db.relationship('HeroPower', backref='power', lazy=True)


class HeroPower(db.Model):
    __tablename__ = 'heropower'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("power.id"), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("hero.id"), nullable=False)
    hero = db.relationship('Hero', backref='powers')
    power = db.relationship('Power', backref='heroes')

    VALID_STRENGTHS = {'Strong', 'Weak', 'Average'}

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in self.VALID_STRENGTHS:
            raise ValueError("Invalid strength value")
        return value
