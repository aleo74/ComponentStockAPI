from datetime import datetime

from bson import ObjectId
from flask_jwt_extended import jwt_required
from app.models.stocks import Stocks
from flask import jsonify
import app
from flask import request


class StockController:

    @classmethod
    @jwt_required()
    def get_one_stock(cls, name):
        stock = cls.find_one({'name': name})

        if stock:
            stock['_id'] = str(stock['_id'])
            return jsonify(stock)
        else:
            # Aucun stock trouvé, renvoyez une réponse avec un code HTTP 404 (Non trouvé)
            return jsonify({'message': f"Stock avec le nom '{name}' introuvable."}), 40

    @classmethod
    @jwt_required()
    def get_stocks_by_name(cls, name):
        stocks_cursor = cls.find({'name': name})
        stocks = list(stocks_cursor)

        if stocks:
            for stock in stocks:
                stock['_id'] = str(stock['_id'])
            return jsonify(stocks)
        else:
            return jsonify({'message': f"Stock avec le nom '{name}' introuvable."}), 40

    @classmethod
    @jwt_required()
    def get_stock_by_id(cls, stock_id):
        stock = cls.find_one({'_id': ObjectId(stock_id)})
        if stock:
            stock['_id'] = str(stock['_id'])
            return jsonify(stock), 200
        else:
            return jsonify({'message': f"Stock avec l'ID '{stock_id}' introuvable."}), 404

    @classmethod
    @jwt_required()
    def get_stocks(cls):
        stocks = cls.find({})
        stock_list = []
        for stock in stocks:
            stock['_id'] = str(stock['_id'])
            stock_list.append(stock)
        return jsonify(stock_list), 200

    @classmethod
    @jwt_required()
    def save_stock(cls):
        data = request.get_json()
        name = data['name']
        desc = data['desc']
        qty = data['qty']
        if cls.save(Stocks(name, desc, qty)):
            response_data = {"message": "Stock enregistre avec succes"}
            return jsonify(response_data), 200

    @classmethod
    def save(cls, stockToSave):
        stockToSave.updated_at = datetime.utcnow()
        result = app.db.db.stocks.insert_one(stockToSave.to_dict())
        inserted_id = result.inserted_id
        if inserted_id:
            return inserted_id
        else:
            None

    @classmethod
    @jwt_required()
    def edit_stock(cls, stock_id):
        data = request.get_json()
        stock = cls.find_one({'_id': ObjectId(stock_id)})

        if stock and 'qty' in data:
            stock['qty'] = data['qty']
            cls.update_one(stock['_id'], stock)

            return jsonify({"message": "Stock mis à jour avec succès"}), 200
        else:
            return jsonify({'message': f"Stock avec l'ID '{stock_id}' introuvable."}), 404

    @classmethod
    def find_one(cls, query):
        return app.db.db.stocks.find_one(query)

    @classmethod
    def find(cls, query):
        return app.db.db.stocks.find(query)

    @classmethod
    def delete_one(cls, query):
        return app.db.db.stocks.delete_one(query)

    @classmethod
    def delete_many(cls, query):
        return app.db.db.stocks.delete_many(query)

    @classmethod
    def update_one(cls, id, query):
        return app.db.db.stocks.update_one({'_id': id}, {'$set': query})
