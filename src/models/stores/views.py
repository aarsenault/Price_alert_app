from flask import Blueprint


store_blueprint = Blueprint('stores', __name__)

# check out a store name
@store_blueprint.route('/store/<string:name>')
def store_page():
    pass


