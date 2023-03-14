from contextlib import nullcontext
from email.policy import default
from operator import truediv
from application import db, BaseModelMixin


class Register(db.Model, BaseModelMixin):

    id = db.Column(db.Integer(), primary_key=True)
    id_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    id_accountingDocument = db.Column(db.Integer(), db.ForeignKey('accounting_document.id'))
    consecutive = db.Column(db.Integer())
    date = db.Column(db.Date())
    id_supplier = db.Column(db.Integer(), db.ForeignKey('supplier.id'))
    observations = db.Column(db.String(150))  
    
    user = db.relationship('User', 
        backref= db.backref('user'))
    
    accountingDocument = db.relationship('AccountingDocument',
        backref=db.backref('accounting_document'))

    supplier = db.relationship('Supplier',
        backref=db.backref('registros'))
    
    def __init__(self, user, accountigDocument, consecutive, date, supplier, observations):
        self.id_user = user['id']
        self.id_accountingDocument = accountigDocument['id']
        self.consecutive = consecutive
        self.date = date
        self.id_supplier = supplier['id']
        self.observations = observations

    def __repr__(self):
        return '<Register' % self.id

class Entry(db.Model, BaseModelMixin):

    id = db.Column(db.Integer(), primary_key=True)
    id_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    id_register = db.Column(db.Integer(), db.ForeignKey('register.id'))
    id_account = db.Column(db.Integer(), db.ForeignKey('account.id'))
    description = db.Column(db.String(150))
    id_supplier = db.Column(db.Integer(), db.ForeignKey('supplier.id'))
    type = db.Column(db.Boolean())
    baseValue = db.Column(db.Float())
    percentage = db.Column(db.Float())
    totalValue = db.Column(db.Float())
    id_formOfPayment = db.Column(db.Integer(), nullable = True)
    id_costCenter = db.Column(db.Integer(), nullable = True)

    user = db.relationship('User', 
        backref= db.backref('user'))
    
    register = db.relationship('Register',
        backref=db.backref('register'))

    account = db.relationship('Account',
        backref=db.backref('account'))
    
    supplier = db.relationship('Supplier',
        backref=db.backref('supplier'))
        

    def __init__(self, user, register, account, description, supplier, type, baseValue, percentage, totalValue, id_formOfPayment, id_costCenter):
        self.id_user = user['id']
        self.id_register = register['id']
        self.id_account = account['id']
        self.description = description
        self.id_supplier = supplier['id']
        self.type =  type
        self.baseValue = baseValue
        self.percentage = percentage
        self.totalValue = totalValue
        self.id_formOfPayment = id_formOfPayment
        self.id_costCenter = id_costCenter

    def __repr__(self):
        return self.id
    