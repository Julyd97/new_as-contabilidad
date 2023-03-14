from application import ma
from accountingDocument.models import AccountingDocument
from marshmallow_sqlalchemy import field_for, auto_field
from marshmallow_sqlalchemy.fields import Nested

# class AccountingDocumentSchema(ma.Schema):
#     id = fields.Integer(dump_only = True)
#     id_user = fields.Integer(required = True)
#     date = fields.Date()
#     description = fields.String()
#     consecutive = fields.Integer()
#     prefix = fields.String()
#     documentType = fields.String()
#     template = fields.String()

class AccountingDocumentSchema(ma.SQLAlchemyAutoSchema):

    id = field_for(AccountingDocument, 'id', dump_only = True)

    class Meta:
        model = AccountingDocument
        load_instance = True