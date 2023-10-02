from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    heropowers = db.relationship('HeroPower', backref='hero', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': [power.as_dict() for power in self.powers]
        }


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    heropowers = db.relationship('HeroPower', backref='power', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class HeroPower(db.Model):
    __tablename__ = 'heropower'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("power.id"), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("hero.id"), nullable=False)

    VALID_STRENGTHS = {'Strong', 'Weak', 'Average'}

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in self.VALID_STRENGTHS:
            raise ValueError("Invalid strength values")
        return value

    def as_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'power': self.power.as_dict()
        }
