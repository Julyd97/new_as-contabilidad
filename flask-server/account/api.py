from email import message
from flask import request, Blueprint
from flask_restful import Api, Resource
from sqlalchemy.orm import aliased

from account.schemas import AccountSchema
from account.models import Account

account_app = Blueprint('account_app', __name__)
account_schema = AccountSchema()

api = Api(account_app)

class AccountListResource(Resource):
    def get(self):
        serial_number = request.args.get('codigo')
        description_text = request.args.get('description')
        filter_childs = request.args.get('childs')
        accounts = Account.query.order_by(Account.serial)
        print(filter_childs)
        if filter_childs !=None :
            accounts1 = Account.query.with_entities(Account.parent_id).filter(Account.parent_id.is_not(None))
            accounts =  Account.query.filter(Account.id.not_in(accounts1)).order_by(Account.serial)
            print(accounts)
        if serial_number == None and description_text == None and filter_childs == None:
            accounts = Account.query.order_by(Account.serial)
        elif serial_number != None and description_text == None:
            accounts = accounts.filter(Account.serial.like(str(serial_number) + '%')).order_by(Account.serial).all()
        elif serial_number == None and description_text != None: 
            accounts = accounts.filter(Account.description.like(str(description_text) + '%')).order_by(Account.description).all()
            if accounts == []:
                result = account_schema.dump(accounts, many=True)
                return  result, 404 
        result = account_schema.dump(accounts, many=True)        
        return result, 201
    def post(self):
        data = request.get_json()
        account_dict = account_schema.load(data)
        account_serial = account_dict['serial']
        current_account = Account.query.filter_by(serial=account_serial).first()
        if(current_account != None):
            return {'message':'La cuenta que intenta crear ya esta creada.','alerta': 'alert-danger','icon':'#exclamation-triangle-fill'}, 404
        else:
            if(len(account_serial) > 1):
                a = verify_parent(account_serial)
                if(a[0] == True):
                    parent_id1 = a[1]
                    level1 = a[2]
                else:
                    return {'message':'La cuenta que intenta crear no tiene una cuenta superior','alerta':'alert-danger','icon':'#exclamation-triangle-fill'},404
            else:
                parent_id1 = None
                level1 = '0'
            account = Account(parent_id = parent_id1,
                                id_user = account_dict['id_user'],
                                level = level1,
                                serial = account_dict['serial'],
                                description = account_dict['description'],
                                portfolio = account_dict['portfolio'],
                                stakeholder = account_dict['stakeholder'],
                                supplier = account_dict['supplier'],
                                costCenter= account_dict['costCenter'],
                                nature = account_dict['nature'],
                                type = account_dict['type']
                        )  
            account.save()
            resp = account_schema.dump(account)
            return {'message':'La cuenta se creo exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
    
    
        
class AccountResource(Resource):
    def get(self, account_id):
        account = Account.get_by_id(account_id)
        if account is None:
            return {'message':'La cuenta no existe.','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}
        resp = account_schema.dump(account)
        return resp
    def put(self, account_id):
        account = Account.get_by_id(account_id)
        if account is None:
            return{'message':'La cuenta no existe', 'alerta':'alert-danger','icon':'#exclamation-triangle-fill'}
        data = request.get_json()
        try:
            account_dict = account_schema.load(data)
            
            account.description = account_dict['description']
            account.portfolio = account_dict['portfolio']
            account.stakeholder = account_dict['stakeholder']
            account.supplier = account_dict['supplier']
            account.costCenter = account_dict['costCenter']
            
            account.save()
            resp = account_schema.dump(account)
            return {'message': 'La cuenta se ha modificado con exito', 'alerta':'alert-success','icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Ocurrio un error modificando la cuenta', 'alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 400
    def  delete(self, account_id):
        account = Account.get_by_id(account_id)
        account_child = Account.query.filter(Account.parent_id.like(account_id)).all()
        if account is None:
            return {'message': 'La cuenta que intenta eliminar no existe', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404
        elif(account_child != []):
            return {'message': 'La cuenta que intenta posee accounts inferiores y no puede ser eliminada', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 400
        try:
            account.delete()
            return {'message': 'La cuenta se elimino con exito', 'alerta':'alert-success', 'icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Un error ocurrio un error eliminando la cuenta seleccionada', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404

api.add_resource(AccountListResource, '/api/v1.0/accounts/', endpoint='accounts_list_resource')
api.add_resource(AccountResource, '/api/v1.0/account/<int:account_id>', endpoint='account_resource')

def verify_parent(child_serial):
    length_child_serial = len(child_serial)
    if(length_child_serial > 2 and length_child_serial % 2 ==0):
        serial_parent = child_serial[0:(length_child_serial-2)]
    elif(length_child_serial == 2):
        serial_parent = child_serial[0:1]
    else:
        return [False]
    parent_account = Account.query.filter_by(serial=serial_parent).first()
    if parent_account ==None:
        return [False]
    else:
        account_level = str(int(parent_account.level)+1)
        parent_id = str(parent_account.id)

        return [True, parent_id, account_level]