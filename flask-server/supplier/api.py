from cgi import print_directory
from flask import request, Blueprint
from flask_restful import Api, Resource

from supplier.schemas import SupplierSchema
from supplier.models import Supplier
from user.schemas import UserSchema
from user.models import User

suppliers_app = Blueprint('suppliers_app', __name__)
supplier_schema = SupplierSchema()

api = Api(suppliers_app)

class SupplierListResource(Resource):
    def get(self):
        cedula_number=request.args.get('numero')
        supplier_name = request.args.get('nombre')
        if cedula_number == None and supplier_name == None:
            suppliers = Supplier.query.order_by(Supplier.documentNumber)
            result = supplier_schema.dump(suppliers, many=True)    
        elif cedula_number != None and supplier_name== None:
            suppliers = Supplier.query.filter(Supplier.documentNumber.like(str(cedula_number) + '%')).order_by(supplier.documentNumber).all()
            result = supplier_schema.dump(suppliers, many=True)
            if suppliers == []:
                return  result, 404
        else:  
            suppliers = Supplier.query.filter(Supplier.firstName.like(str(supplier_name) + '%')).order_by(supplier.documentNumber).all()
            result = supplier_schema.dump(suppliers, many=True)
            if suppliers == []:
                return  result, 404
        return result, 201
    def post(self):
        data = request.get_json()
        supplier_dict = supplier_schema.load(data)
        documentnumber = supplier_dict['documentNumber']
        id_user = supplier_dict['id_user']

        user = User.query.get_by_id(id_user)
        current_supplier= Supplier.query.filter_by(documentNumber = documentnumber).first()
        print(supplier_dict)
        
        if(current_supplier != None):
            return {'message': 'El proveedor que intenta crear ya esta creado.', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404
        else:
            supplier = Supplier(    user = user,
                                    documentType = supplier_dict['documentType'],
                                    documentNumber = supplier_dict['documentNumber'],
                                    country = supplier_dict['country'], department = supplier_dict['department'],
                                    municipality = supplier_dict['municipality'],
                                    firstName = supplier_dict['firstName'],
                                    secondName = supplier_dict['secondName'],
                                    firstLastName = supplier_dict['firstLastName'],
                                    secondLastName = supplier_dict['secondLastName'],
                                    address = supplier_dict['address'],
                                    phone = supplier_dict['phone'],
                                    mail = supplier_dict['mail'],
                                    zipCode = supplier_dict['zipCode']
            )

            supplier.save()
            resp = supplier_schema.dump(supplier)
            return {'message':'El proveedor se creo exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
    
    
        
class SupplierResource(Resource):
    def get(self, supplier_id):
        supplier = supplier.get_by_id(supplier_id)
        if supplier is None:
            return {'message': 'El proveedor que esta buscando no existe', 'alerta':'alert-warning', 'icon':'#exclamation-triangle-fill'}, 404
        resp = supplier_schema.dump(supplier)
        return resp
    def put(self, supplier_id):
        supplier = Supplier.get_by_id(supplier_id)
        if supplier is None:
            return {'message': 'El proveedor que esta modificando no existe', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404
        data = request.get_json()
        supplier_dict = supplier_schema.load(data)
        print(data)
        try:
            supplier_dict = supplier_schema.load(data)
            supplier.documentType = supplier_dict['documentType']
            supplier.documentNumber = supplier_dict['documentNumber']
            supplier.country = supplier_dict['country']
            supplier.department = supplier_dict['department']
            supplier.municipality = supplier_dict['municipality']
            supplier.firstName = supplier_dict['firstName']
            supplier.secondName = supplier_dict['secondName']
            supplier.firstLastName = supplier_dict['firstLastName']
            supplier.secondLastName = supplier_dict['secondLastName']
            supplier.address = supplier_dict['address']
            supplier.phone = supplier_dict['phone']
            supplier.mail = supplier_dict['mail']
            supplier.zipCode = supplier_dict['zipCode']
            
            supplier.save()
            resp = supplier_schema.dump(supplier)
            return {'message':'El proveedor se modifico exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Ocurrio un error modificando el proveedor','alerta':'alert-warning', 'icon':'#exclamation-triangle-fill'}, 400
    def  delete(self, supplier_id):
        supplier = Supplier.get_by_id(supplier_id)
        if supplier is None:
            return {'message': 'El proveedor que intenta eliminar no existe', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404
        try:
            supplier.delete()
            return {'message': 'El proveedor se elimino exitosamente', 'alerta':'alert-success', 'icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Ocurrio un error eliminando el proveedor','alerta':'alert-warning', 'icon':'#exclamation-triangle-fill'}, 400

api.add_resource(SupplierListResource, '/api/v1.0/suppliers/', endpoint='suppliers_list_resource')
api.add_resource(SupplierResource, '/api/v1.0/supplier/<int:supplier_id>', endpoint='supplier_resource')