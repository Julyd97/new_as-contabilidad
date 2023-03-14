from flask import request, Blueprint
from flask_restful import Api, Resource

from accountingDocument.schemas import AccountingDocumentSchema
from accountingDocument.models import AccountingDocument

accountingDocument_app = Blueprint('accountingDocument_app', __name__)
accountingDocument_schema = AccountingDocumentSchema()

api = Api(accountingDocument_app)

class AccountingDocumentListResource(Resource):
    def get(self, cedula_number=None):
        if cedula_number == None:
            documents = AccountingDocument.get_all()
            result = accountingDocument_schema.dump(documents, many=True)
        else:  
            suppliers = AccountingDocument.query.filter(AccountingDocument.documentNumber.like(str(cedula_number) + '%')).all()
            if suppliers == []:
                return  {'message': 'El documento buscado no existe','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 404
            else:         
                result = accountingDocument_schema.dump(suppliers, many=True)
        return result, 201
    def post(self):
        data = request.get_json()
        accountingDocument_dict = accountingDocument_schema.load(data)
        documents = AccountingDocument(date = accountingDocument_dict['date'],
                                        description = accountingDocument_dict['description'],
                                        consecutive = accountingDocument_dict['consecutive'],
                                        prefix = accountingDocument_dict['prefix'],
                                        documentType = accountingDocument_dict['documentType'],
                                        template = accountingDocument_dict['template']
        )  
        documents.save()
        resp = accountingDocument_schema.dump(documents)
        return {'message':'Elte documento se creo exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
    
    
        
class AccountingDocumentResource(Resource):
    def get(self, document_id):
        document = AccountingDocument.get_by_id(document_id)
        if document is None:
            return  {'message': 'El documento buscado no existe','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 404
        resp = accountingDocument_schema.dump(document)
        return resp
    def put(self, document_id):
        document = AccountingDocument.get_by_id(document_id)
        data = request.get_json()
        if document is None:
            return  {'message': 'El documento buscado no existe','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 404
        try:
            document_dict = accountingDocument_schema.load(data)
            print(document_dict)
            document.date = document_dict['date']
            document.description = document_dict['description']
            document.consecutive = document_dict['consecutive']
            document.prefix = document_dict['prefix']
            document.documentType = document_dict['documentType']
            
            
            document.save()
            resp = accountingDocument_schema.dump(document)
            return {'message':'El documento se modifico exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Ocurrio un error modificando el proveedor','alerta':'alert-warning','icon':'#exclamation-triangle-fill'}, 400
    def  delete(self, document_id):
        document = AccountingDocument.get_by_id(document_id)
        if document is None:
            return  {'message': 'El documento buscado no existe','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 404
        try:
            document.delete()
            return {'message':'El documento se elimino exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Un error ocurrio un error eliminando el proveedor','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 400

api.add_resource(AccountingDocumentListResource, '/api/v1.0/accountingdocuments/', endpoint='accountingdocuments_list_resource')
api.add_resource(AccountingDocumentResource, '/api/v1.0/accountingdocument/<int:document_id>', endpoint='accountingdocument_resource')