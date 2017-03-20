from flask import Flask

from src.common.database import Database

app = Flask(__name__)


# TODO
# not totally sure what this line means
app.config.from_object('config')

app.secret_key = '123'

@app.before_first_request
def init_db():
    Database.initialize()

from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")