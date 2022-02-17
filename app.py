from flask import Flask, session


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3636@localhost:5432/TechEdge'
app.config['SECRET_KEY'] = '3636'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




from db_helper.db_models import *
db.create_all()


from controller import techedge
app.register_blueprint(techedge)