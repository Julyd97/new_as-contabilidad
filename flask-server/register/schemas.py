from application import ma
from register.models import Register, Entry
from marshmallow_sqlalchemy import field_for, auto_field
from marshmallow_sqlalchemy.fields import Nested

# class RegisterSchema(ma.Schema):
#     id = fields.Integer(dump_only = True)
#     id_user = fields.Integer(required = True)
#     id_accountingDocument = fields.Integer()
#     consecutive = fields.Integer()
#     date = fields.Date()
#     id_supplier = fields.Integer(required=True)
#     observations = fields.String()


class RegisterSchema(ma.SQLAlquemyAutoSchema):
    
    id = field_for(Register, 'id', dump_only = True)

    class Meta:
        model = Register
        load_instance = True

# class EntrySchema(ma.Schema):
#     id = fields.Integer(dump_only = True)
#     id_user = fields.Integer(required = True)
#     id_register = fields.Integer()
#     id_account = fields.Integer()
#     description  = fields.String()
#     id_supplier = fields.Integer()
#     type = fields.Boolean()
#     baseValue = fields.Float()
#     percentage = fields.Float()
#     totalValue = fields.Float()
#     id_formOfPayment = fields.Integer(allow_none = True)
#     id_costCenter = fields.Integer(allow_none = True)

class EntrySchema(ma.SQlAlchemyAutoSchema):
    
    id = field_for(Entry, 'id', dump_only = True)

    class Meta:
        model = Entry
        load_instance = True
