from datetime import datetime
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
            # Stock trouvé, renvoyez-le en tant que réponse JSON
            stock['_id'] = str(stock['_id'])
            return jsonify(stock)
        else:
            # Aucun stock trouvé, renvoyez une réponse avec un code HTTP 404 (Non trouvé)
            return jsonify({'message': f"Stock avec le nom '{name}' introuvable."}), 40

    @classmethod
    @jwt_required()
    def get_stocks(cls, name):
        stocks_cursor = cls.find({'name': name})
        stocks = list(stocks_cursor)

        if stocks:
            for stock in stocks:
                stock['_id'] = str(stock['_id'])
            return jsonify(stocks)
        else:
            return jsonify({'message': f"Stock avec le nom '{name}' introuvable."}), 40

    @classmethod
    def save_stock(cls):
        data = request.get_json()
        name = data['name']
        desc = data['desc']
        qty = data['qty']
        print(name)
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
