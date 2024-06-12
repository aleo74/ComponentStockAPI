from flask_jwt_extended import create_access_token
from flask import request, jsonify
from app.models.User import User
from datetime import datetime
import app


class AuthController:

    @classmethod
    def register(cls):
        data = request.get_json()
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']
            email = data['email']

            # Créez un nouvel utilisateur
            user = User(username=username, password=password, email=email)

            try:
                idUser = cls.save(user)
                return jsonify({'message': f'Utilisateur enregistré avec succès : {str(idUser)}'}), 201
            except Exception as e:
                return jsonify({'message': f'Échec de l\'enregistrement de l\'utilisateur: {str(e)}'}), 400
        else:
            return jsonify({'message': 'Données de formulaire incorrectes'}), 400

    @classmethod
    def login(cls):
        data = request.get_json()
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']

            userData = cls.find_one({'username': username})

            if userData:
                user = User(username=userData['username'], password=userData['password'], email=userData['email'])

                if user.check_password(password):
                    access_token = create_access_token(identity=username)

                    return jsonify({'access_token': access_token}), 200
                else:
                    return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
            else:
                return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
        else:
            return jsonify({'message': 'Données de formulaire incorrectes'}), 400

    @classmethod
    def save(cls, userToSave):
        userToSave.updated_at = datetime.utcnow()
        result = app.db.db.Users.insert_one(userToSave.to_dict())
        inserted_id = result.inserted_id
        if inserted_id:
            return inserted_id
        else:
            None

    @classmethod
    def find_one(cls, query):
        return app.db.db.Users.find_one(query)
