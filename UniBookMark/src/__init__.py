# from config import Config
# from controllers import bookmark_controller, user_controller
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from models import bookmark, user

# db = SQLAlchemy()


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)

#     app.register_blueprint(user_controller.user_bp)
#     app.register_blueprint(bookmark_controller.bookmark_bp)

#     with app.app_context():
#         db.create_all()

#     return app
