import os
from datetime import datetime
from bson import ObjectId
from flask_jwt_extended import jwt_required
from app.models.Tags import Tags
from flask import jsonify, request
import app
import json
from bson.json_util import dumps


class TagsController:

    @classmethod
    @jwt_required()
    def get_tags(cls):
        tags = cls.find({})
        tags_list = []
        for tag in tags:
            tag['_id'] = str(tag['_id'])
            tags_list.append(tag)
        return jsonify(tags_list), 200

    @classmethod
    @jwt_required()
    def get_tag_by_id(cls, tag_id):
        tag = cls.find_one({'_id': ObjectId(tag_id)})
        if tag:
            tag['_id'] = str(tag['_id'])
            return jsonify(tag), 200
        else:
            return jsonify({'message': f"Tag avec l'ID '{tag_id}' introuvable."}), 404

    @classmethod
    @jwt_required()
    def save_tag(cls):
        data = request.get_json()
        name = data['name']
        desc = data['description']
        color = data['color']

        saved_tag = cls.save(Tags(name, desc, color))
        if saved_tag:
            response_data = {"message": "Tag enregistre avec succes", "tag": saved_tag}
            return jsonify(response_data), 200

    @classmethod
    @jwt_required()
    def edit_tag(cls, tag_id):
        data = request.get_json()
        tag = cls.find_one({'_id': ObjectId(tag_id)})

        if tag:
            tag['name'] = data['name']
            tag['description'] = data['description']
            tag['color'] = data['color']
            tag['updated_at'] = datetime.utcnow()

            cls.update_one(tag['_id'], tag)
            return jsonify({"message": "Tag mis à jour avec succès"}), 200
        else:
            return jsonify({'message': f"Tag avec l'ID '{tag_id}' introuvable."}), 404

    @classmethod
    def save(cls, tagToSave):
        tagToSave.updated_at = datetime.utcnow()
        result = cls.insert_one(tagToSave.to_dict())
        inserted_id = result.inserted_id
        if inserted_id:
            tagToSave._id = str(inserted_id)
            saved_tag = tagToSave.to_dict()
            return saved_tag
        else:
            None

    @classmethod
    @jwt_required()
    def delete_tag(cls, tag_id):
        tag = cls.find_one({'_id': ObjectId(tag_id)})
        if tag:
            cls.delete_one(tag)
            return ({'message': "Supression effectuée"}), 200
        else:
            return jsonify({'message': f"Tag avec l'ID '{tag}' introuvable."}), 404

    @classmethod
    @jwt_required()
    def delete_tag_and_update_stocks(cls, tag_id):
        tag = cls.find_one({'_id': ObjectId(tag_id)})
        if tag:
            # Supprimer le tag
            cls.delete_one(tag)

            # Récupérer tous les stocks
            stocks = app.db.db.stocks.find({'tags': {'$regex': str(tag_id)}})
            for stock in stocks:
                tags = json.loads(stock['tags'])
                tags = [t for t in tags if t['_id'] != str(tag_id)]
                app.db.db.stocks.update_one(
                    {'_id': stock['_id']},
                    {'$set': {'tags': json.dumps(tags)}}
                )

            return ({'message': "Tag et références dans les stocks supprimés avec succès"}), 200
        else:
            return jsonify({'message': f"Tag avec l'ID '{tag_id}' introuvable."}), 404



    @classmethod
    def find_one(cls, query):
        return app.db.db.tags.find_one(query)

    @classmethod
    def find(cls, query):
        return app.db.db.tags.find(query)

    @classmethod
    def insert_one(cls, query):
        return app.db.db.tags.insert_one(query)

    @classmethod
    def delete_one(cls, query):
        return app.db.db.tags.delete_one(query)

    @classmethod
    def delete_many(cls, query):
        return app.db.db.tags.delete_many(query)

    @classmethod
    def update_one(cls, id, query):
        return app.db.db.tags.update_one({'_id': id}, {'$set': query})