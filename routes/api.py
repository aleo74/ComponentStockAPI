from flask import Blueprint
from app.controllers.stock import StockController
from app.controllers.auth import AuthController
from app.controllers.tags import TagsController

main_bp = Blueprint('main', __name__)


main_bp.add_url_rule('/save_stock', 'save_stock', StockController.save_stock, methods=['POST'])
main_bp.add_url_rule('/get_one_stock/<string:name>', 'get_one_stock', StockController.get_one_stock)
main_bp.add_url_rule('/get_stocks/<string:name>', 'get_stocks_by_name', StockController.get_stocks_by_name)
main_bp.add_url_rule('/get_stock_id/<string:stock_id>', 'get_stocks_by_id', StockController.get_stock_by_id)
main_bp.add_url_rule('/get_stocks', 'get_stocks', StockController.get_stocks)
main_bp.add_url_rule('/edit_stock/<string:stock_id>', 'edit_stock', StockController.edit_stock, methods=['PUT'])
main_bp.add_url_rule('/delete_stock/<string:stock_id>', 'delete_stock', StockController.delete_stock, methods=['DELETE'])
main_bp.add_url_rule('/images/<path:filename>', 'get_image', StockController.get_image)

main_bp.add_url_rule('/save_tag', 'save_tag', TagsController.save_tag, methods=['POST'])
main_bp.add_url_rule('/get_tags', 'get_tags', TagsController.get_tags)
main_bp.add_url_rule('/get_tag_id/<string:tag_id>', 'get_tag_by_id', TagsController.get_tag_by_id)
main_bp.add_url_rule('/edit_tag/<string:tag_id>', 'edit_tag', TagsController.edit_tag, methods=['PUT'])
main_bp.add_url_rule('/delete_tag/<string:tag_id>', 'delete_tag', TagsController.delete_tag, methods=['DELETE'])
main_bp.add_url_rule('/delete_tag_and_update_stocks/<string:tag_id>', 'delete_tag_and_update_stocks', TagsController.delete_tag_and_update_stocks, methods=['DELETE'])

# AUTH
main_bp.add_url_rule('/register', 'register', AuthController.register, methods=['POST'])
main_bp.add_url_rule('/login', 'login', AuthController.login, methods=['POST'])
