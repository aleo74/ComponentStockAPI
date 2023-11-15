from flask import Blueprint
from app.controllers.stock import StockController
from app.controllers.auth import AuthController

main_bp = Blueprint('main', __name__)


main_bp.add_url_rule('/save_stock', 'save_stock', StockController.save_stock, methods=['POST'])
main_bp.add_url_rule('/get_one_stock/<string:name>', 'get_one_stock', StockController.get_one_stock)
main_bp.add_url_rule('/get_stocks/<string:name>', 'get_stocks', StockController.get_stocks)


# AUTH
main_bp.add_url_rule('/register', 'register', AuthController.register, methods=['POST'])
main_bp.add_url_rule('/login', 'login', AuthController.login, methods=['POST'])
