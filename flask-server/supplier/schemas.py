from application import ma
from supplier.models import Supplier
from marshmallow_sqlalchemy import field_for, auto_field
from marshmallow_sqlalchemy.fields import Nested

# class SupplierSchema(ma.Schema):
#     id = fields.Integer(dump_only = True)
#     id_user = fields.Integer(required = True)
#     documentType = fields.String()
#     documentNumber = fields.Integer()
#     country = fields.String()
#     department = fields.String()
#     municipality = fields.String()
#     firstName = fields.String()
#     secondName = fields.String()
#     firstLastName = fields.String()
#     secondLastName = fields.String()
#     address = fields.String()
#     phone = fields.Integer(allow_none = True)
#     mail = fields.String()
#     zipCode = fields.Integer(allow_none = True)

class SupplierSchema(ma.SQLAlchemyAutoSchema):
    id = field_for(Supplier, 'id', dump_only = True)

    class Meta:
        model = Supplier
        load_instance = True
