from application import ma
from user.models import User
from marshmallow_sqlalchemy import field_for, auto_field
from marshmallow_sqlalchemy.fields import Nested

class UserSchema(ma.SQLAlchemyAutoSchema):
    id = field_for(User, 'id', dunp_only = True)

    class Meta:
        model = User
        load_instance = True
