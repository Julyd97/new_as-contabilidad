from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_marshmallow import Marshmallow

from supplier.error_handling import ObjectNotFound, AppErrorBaseClass
# setup db
db = SQLAlchemy()
ma = Marshmallow()

#methods
class BaseModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()
    

def create_app(** config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    app.config.update(config_overrides)

    # initialize db
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # import blueprints
    
    from account.api import account_app
    from supplier.api import suppliers_app
    from accountingDocument.api import accountingDocument_app
    from register.api import register_app
    # register blueprints
    
    app.register_blueprint(account_app)
    app.register_blueprint(suppliers_app)
    app.register_blueprint(accountingDocument_app)
    app.register_blueprint(register_app)
    return app
