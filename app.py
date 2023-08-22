import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder='routes')

    from mongo import MongoConnection
    mongo = MongoConnection.get_instance()

    from routes.users import users
    app.register_blueprint(users, url_prefix="/users/")

    from routes.transactions import transactions
    app.register_blueprint(transactions, url_prefix="/transactions/")

    from routes.smart_contracts import smart_contracts
    app.register_blueprint(smart_contracts, url_prefix="/smart_contracts/")

    from routes.nfts import nfts
    app.register_blueprint(nfts, url_prefix="/nfts/")

    return app


# @app.route('/')
# def hello_world():  # put application's code here
#     # return 'Hello World!'
#     # print(mongo.db.users)
#     return render_template('index.html')


if __name__ == '__main__':
    SECRET_KEY = os.getenv('SECRET_KEY') or 'this is a secret'
    # print(SECRET_KEY)
    app = create_app()

    app.config['SECRET_KEY'] = SECRET_KEY

    app.run(host="127.0.0.1", debug=True, load_dotenv=True)
