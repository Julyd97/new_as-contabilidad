import imp
from flask import request, Blueprint
from flask_restful import Api, Resource
from sqlalchemy import update
from application import db
from user.api import login_required
from user.schemas import UserSchema
from user.models import User
from register.schemas import RegisterSchema
from register.models import Register
from register.schemas import EntrySchema
from register.models import Entry
from account.models import Account
from account.schemas import AccountSchema
from supplier.models import Supplier
from supplier.schemas import SupplierSchema
from accountingDocument.models import AccountingDocument
from accountingDocument.schemas import AccountingDocumentSchema

register_app = Blueprint('register_app', __name__)
register_schema = RegisterSchema()
entry_schema = EntrySchema()
supplier_schema = SupplierSchema()
account_schema = AccountSchema()
accountingDocument_schema = AccountingDocumentSchema()
user_schema = UserSchema()

api = Api(register_app)

class RegisterListResource(Resource):
    @login_required
    def get(self):
        consecutive = request.args.get('consecutive')
        registers = Register.query.order_by(Register.consecutive)
        if consecutive !=None :
            registers = Register.query.filter(Register.consecutive.like(str(consecutive)+ '%')).order_by(Register.consecutive).all()
            if registers == []:
                result = register_schema.dump(registers, many=True)
                return  result, 404 
        result = register_schema.dump(registers, many=True)        
        return result, 201
    def post(self):
        data = request.get_json()        
        data_entrys = data['entry']
        data.pop('entry')
        data_register = data
        try:
            register_dict = register_schema.load(data_register)
        except:
            return {'message':'La creacion del registro no fue satisfactoria.','alerta': 'alert-danger','icon':'#exclamation-triangle-fill'}, 404
        consecutive_register = register_dict['consecutive']
        date_register = register_dict['date']
        id_accountingDocument = register_dict['id_accountingDocument']
        id_supplier = register_dict['id_supplier']
        id_user = register_dict['id_user']

        user = user_schema.dump (User.get_by_id(id_user))
        accountingDocument = accountingDocument_schema.dump(AccountingDocument.get_by_id(id_accountingDocument))
        suppliers = supplier_schema.dump(Supplier.get_by_id(id_supplier))
        current_register = Register.query.filter_by(id_accountingDocument = id_accountingDocument, consecutive = consecutive_register).first()

        if(current_register != None):
            return {'message':'La cuenta que intenta crear ya esta creada.','alerta': 'alert-danger','icon':'#exclamation-triangle-fill'}, 404
        else:
            try:   
                register = Register(
                                    user = user,
                                    accountingDocument = accountingDocument,
                                    consecutive = register_dict['consecutive'],
                                    date = register_dict['date'],
                                    supplier = suppliers,
                                    observations = register_dict['observations'],
                            )  
                doc=AccountingDocument.get_by_id(id_accountingDocument)
                doc.consecutive = consecutive_register
                doc.date = date_register
                
                
                db.session.add(register)
                db.session.add(doc)
                db.session.flush()
                debitValue = 0
                creditValue = 0
                for entrydata in data_entrys:
                    try:
                        entry_dict = entry_schema.load(entrydata)
                    except:
                        {'message':'Fallo la creación de los entrys.','alerta': 'alert-danger','icon':'#exclamation-triangle-fill'}, 404
                    
                    id_register = register.id
                    id_user = entry_dict['id_user']
                    id_account = entry_dict['id_account']
                    id_supplier = entry_dict['id_supplier']
                    typeValue = entry_dict['type']
                    totalValue = entry_dict['totalValue']
                    
                    user = user_schema.dump(User.get_by_id(id_user))
                    registers = register_schema.dump(Register.get_by_id(id_register))
                    accounts = account_schema.dump(Account.get_by_id(id_account))
                    suppliers = supplier_schema.dump(Supplier.get_by_id(id_supplier))

                    if typeValue == True:
                        debitValue += totalValue
                    elif typeValue == False:
                        creditValue += totalValue


                    entry = Entry(
                                        register = registers,
                                        user = user,
                                        account = accounts,
                                        description = entry_dict['description'],
                                        supplier = suppliers,
                                        type = entry_dict['type'],
                                        baseValue = entry_dict['baseValue'],
                                        percentage = entry_dict['percentage'],
                                        totalValue = entry_dict['totalValue'],
                                        id_formOfPayment = entry_dict['id_formOfPayment'],
                                        id_costCenter = entry_dict['id_costCenter']
                                )  
                    db.session.add(entry)
                    db.session.flush()

                if creditValue != debitValue:
                    db.session.rollback()
                    return {'message':'Los valores debitos y creditos no concuerdan','alerta': 'alert-danger','icon':'#exclamation-triangle-fill'}, 404
                
                resp = register_schema.dump(register)
                db.session.commit()
                
                return {'message':'El registro se creo exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
            except:
                # stmt=(update(AccountingDocument).where(AccountingDocument.id == id_accountingDocument).values(consecutive = consecutive_registro))
                # print(registro.id)
                # print(stmt)
                print('ha fallado')
                db.session.rollback()
                return {'message':'Fallo la creacion del registro','alerta': 'alert-danger','icon':'#exclamation-triangle-fill'}, 404
    
    
        
class RegisterResource(Resource):
    def get(self, register_id):
        register = Register.get_by_id(register_id)
        if register is None:
            return {'message':'El registro no existe.','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}
        resp = register_schema.dump(register)
        return resp
    def put(self, register_id):
        register = Register.get_by_id(register_id)
        if register is None:
            return{'message':'El registro no existe', 'alerta':'alert-danger','icon':'#exclamation-triangle-fill'}
        data = request.get_json()
        try:
            register_dict = register_schema.load(data)
            
            register.consecutive = register_dict['consecutive']
            register.date = register_dict['date']
            register.id_supplier = register_dict['id_supplier']
            register.observations = register_dict['observations']
            
            register.save()
            resp = register_schema.dump(register)
            return {'message': 'El registro se ha modificado con exito', 'alerta':'alert-success','icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Ocurrio un error modificando el registro', 'alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 400
    def  delete(self, register_id):
        register = Register.get_by_id(register_id)
        if register is None:
            return {'message': 'La cuenta que intenta eliminar no existe', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404
        try:
            register.delete()
            return {'message': 'La cuenta se elimino con exito', 'alerta':'alert-success', 'icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Un error ocurrio un error eliminando la cuenta seleccionada', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404

api.add_resource(RegisterListResource, '/api/v1.0/registers/', endpoint='register_list_resource')
api.add_resource(RegisterResource, '/api/v1.0/register/<int:register_id>', endpoint='register_resource')





class EntryListResource(Resource):
    def get(self):
        id_register = request.args.get('id_register')
        entrys = Entry.query.order_by(Entry.id_register)
        if id_register !=None :
            entrys = Entry.query.filter(Entry.id_register.like(str(id_register))).order_by(Entry.id_register).all()
            if entrys == []:
                result = entry_schema.dump(entrys, many=True)
                return  result, 404 
        result = entry_schema.dump(entrys, many=True)        
        return result, 201
    def post(self):
        data = request.get_json()
        
        for entrydata in data:
            entry_dict = entry_schema.load(entrydata)
            id_register = entry_dict['id_register']
            id_account = entry_dict['id_account']
            id_supplier = entry_dict['id_supplier']
            registers = register_schema.dump(Register.get_by_id(id_register))
            accounts = account_schema.dump(Account.get_by_id(id_account))
            suppliers = supplier_schema.dump(Supplier.get_by_id(id_supplier))

            entry = Entry(
                                register = registers,
                                account = accounts,
                                description = entry_dict['description'],
                                supplier = suppliers,
                                type = entry_dict['type'],
                                baseValue = entry_dict['baseValue'],
                                percentage = entry_dict['percentage'],
                                totalValue = entry_dict['totalValue'],
                                id_formOfPayment = entry_dict['id_formOfPayment'],
                                id_costCenter = entry_dict['id_costCenter']
                        )  
            entry.save()
            return {'message':'El entry se creo exitosamente','alerta':'alert-success','icon':'#check-circle-fill'}, 201
    
    
        
class EntryResource(Resource):
    def get(self, entry_id):
        entry = Entry.get_by_id(entry_id)
        if entry is None:
            return {'message':'El entry no existe.','alerta':'alert-danger','icon':'#exclamation-triangle-fill'}
        resp = entry_schema.dump(entry)
        return resp
    def put(self, entry_id):
        entry = Entry.get_by_id(entry_id)
        if entry is None:
            return{'message':'El entry no existe', 'alerta':'alert-danger','icon':'#exclamation-triangle-fill'}
        data = request.get_json()
        try:
            entry_dict = entry_schema.load(data)
            
            entry.id_register = entry_dict['id_register']
            entry.id_account = entry_dict['id_account']
            entry.description = entry_dict['description']
            entry.id_supplier = entry_dict['id_supplier']
            entry.type = entry_dict['type']
            entry.baseValue = entry_dict['baseValue']
            entry.percentage = entry_dict['percentage']
            entry.totalValue = entry_dict['totalValue']
            entry.id_formOfPayment = entry_dict['id_formOfPayment']
            entry.id_costCenter = entry_dict['id_costCenter']
            
            entry.save()
            resp = entry_schema.dump(entry)
            return {'message': 'El asiento se ha modificado con exito', 'alerta':'alert-success','icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Ocurrio un error modificando el asiento', 'alerta':'alert-danger','icon':'#exclamation-triangle-fill'}, 400
    def  delete(self, entry_id):
        entry = Entry.get_by_id(entry_id)
        if entry is None:
            return {'message': 'El entry que intenta eliminar no existe', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404
        try:
            entry.delete()
            return {'message': 'El entry se elimino con exito', 'alerta':'alert-success', 'icon':'#check-circle-fill'}, 201
        except:
            return {'message': 'Un error ocurrio un error eliminando el entry seleccionada', 'alerta':'alert-danger', 'icon':'#exclamation-triangle-fill'}, 404

api.add_resource(EntryListResource, '/api/v1.0/entrys/', endpoint='entry_list_resource')
api.add_resource(EntryResource, '/api/v1.0/entry/<int:entry_id>', endpoint='entry_resource')