from flask import request, Blueprint, Flask, redirect,session, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt,required, JWTManager
from flask_restful import Api, Resource
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from functools import wraps

from user.models import User
from user.schemas import UserSchema
from application import db
from settings import mail_settings, MAIL_USERNAME, SECRET_KEY

#Create Blueprint of Users
user_app = Blueprint('user_app', __name__)
user_schema = UserSchema()

user_app.config["JWT_SECRET_KEY"] = "TOBBY1210"
jwt = JWTManager(user_app) 
api = Api(user_app)
# Mail settings 

app = Flask(__name__)
app.config.update(mail_settings)
mail = Mail(app)

ts = URLSafeTimedSerializer(secret_key=SECRET_KEY, salt = 'recover-key')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id') is None:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def send_email(subject,recipients,body):
     with app.app_context():
            msg = Message(subject=subject,
                    sender=MAIL_USERNAME,
                      recipients=recipients, 
                    body=body)
            mail.send(msg)

class UserRegister(Resource):
    def post(self):
        full_name = request.args.get('full_name')
        telephone = request.args.get('telephone')
        email = request.args.get('email')
        password = request.args.get('password')
        college_name = request.args.get('college_name')
        college_direction = request.args.get('college_direction')
        college_nit = request.args.get('college_nit')

        user = User.query.filter_by(email = email).first()
        if user:
             return {'message': 'El usuario ingresado ya ha sido registrado, porfavor ingrese con el mismo'}

        new_user = User(
                    full_name=full_name,
                    telephone=telephone,
                    email=email,
                    password=generate_password_hash(password),
                    college_name=college_name,
                    college_direction=college_direction,
                    college_nit=college_nit
        )
        db.session.add(new_user)
        db.session.commit()
        
