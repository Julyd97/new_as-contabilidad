from application import ma
from account.models import Account
from marshmallow_sqlalchemy import field_for, auto_field
from marshmallow_sqlalchemy.fields import Nested

# class AccountSchema(ma.Schema):
#     id = fields.Integer(dump_only = True)
#     id_user = fields.Integer(required = True)
#     parent_id = fields.Integer(allow_none = True)
#     level = fields.String()
#     serial = fields.String()
#     description = fields.String()
#     portfolio = fields.Boolean()
#     stakeholder = fields.Boolean()
#     supplier = fields.Boolean()
#     costCenter = fields.Boolean()
#     nature = fields.Boolean()
#     type =  fields.String()

class AccountSchema(ma.SQLAlchemyAutoSchema):
    id = field_for(Account, 'id', dump_only = True)

    class Meta:
        model = Account
        load_instance = True

        