from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)

class Doacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    doador = db.Column(db.String(100), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship('Item')
