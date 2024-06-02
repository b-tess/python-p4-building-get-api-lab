#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    all_bakeries = []
    for bakery in bakeries:
        all_bakeries.append(bakery.to_dict())

    response = make_response(all_bakeries, 200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id = id).first()
    if bakery:
        response = bakery.to_dict()
        status = 200
    else:
        response = {'message': f'No bakery {id} found.'}
        status = 404
    
    return make_response(response, status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = [baked_good.to_dict(rules=('-bakery',)) for baked_good in baked_goods]
    return make_response(response, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(most_expensive.to_dict(rules=('-bakery',)), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
