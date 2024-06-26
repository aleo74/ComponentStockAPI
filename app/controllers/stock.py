import os
from datetime import datetime

from bson import ObjectId
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app.models.stocks import Stocks
from flask import jsonify, send_from_directory, request
import app
from bson.json_util import dumps


class StockController:
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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
            return jsonify({'message': f"Stock avec le nom '{name}' introuvable."}), 404

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
    def delete_stock(cls, stock_id):
        stock = cls.find_one({'_id': ObjectId(stock_id)})
        if stock:
            cls.delete_one(stock)
            return ({'message': "Supression effectuée"}), 200
        else:
            return jsonify({'message': f"Stock avec l'ID '{stock_id}' introuvable."}), 404

    @classmethod
    @jwt_required()
    def save_stock(cls):
        data = request.form.to_dict()
        if not data:
            data = request.get_json()
        name = data['name']
        desc = data['description']
        qty = data['qty']
        tags = data['tags']
        filename = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                if file and cls.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # TODO : move folder name in env file
                    file.save(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Downloads')), filename))
        saved_stock = cls.save(Stocks(name, desc, qty, filename, tags))
        if saved_stock:
            response_data = {"message": "Stock enregistre avec succes", "stock": saved_stock}
            return jsonify(response_data), 200

    @classmethod
    def save(cls, stockToSave):
        stockToSave.updated_at = datetime.utcnow()
        result = cls.insert_one(stockToSave.to_dict())
        inserted_id = result.inserted_id
        if inserted_id:
            stockToSave._id = str(inserted_id)
            saved_stock = stockToSave.to_dict()
            return saved_stock
        else:
            None

    @classmethod
    @jwt_required()
    def edit_stock(cls, stock_id):
        data = request.form.to_dict()
        if not data:
            data = request.get_json()
        print(data)
        stock = cls.find_one({'_id': ObjectId(stock_id)})

        if stock and 'qty' in data:
            stock['qty'] = data['qty']
            stock['name'] = data['name']
            stock['description'] = data['description']
            stock['updated_at'] = datetime.utcnow()
            stock['tags'] = data['tags']

            if 'image' in request.files:
                file = request.files['image']
                if file.filename != '':
                    if file and cls.allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(
                            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Downloads')),
                                         filename))
                        stock['image_link'] = filename

            cls.update_one(stock['_id'], stock)
            return jsonify({"message": "Stock mis à jour avec succès"}), 200
        else:
            return jsonify({'message': f"Stock avec l'ID '{stock_id}' introuvable."}), 404

    @classmethod
    @jwt_required()
    def get_image(cls, filename):
        return send_from_directory(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Downloads'))), filename)

    @classmethod
    def find_one(cls, query):
        return app.db.db.stocks.find_one(query)

    @classmethod
    def find(cls, query):
        return app.db.db.stocks.find(query)

    @classmethod
    def insert_one(cls, query):
        return app.db.db.stocks.insert_one(query)

    @classmethod
    def delete_one(cls, query):
        return app.db.db.stocks.delete_one(query)

    @classmethod
    def delete_many(cls, query):
        return app.db.db.stocks.delete_many(query)

    @classmethod
    def update_one(cls, id, query):
        return app.db.db.stocks.update_one({'_id': id}, {'$set': query})

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS
