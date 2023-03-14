from application import db, BaseModelMixin

class Supplier(db.Model, BaseModelMixin):

    id = db.Column(db.Integer(), primary_key=True)
    id_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    documentType = db.Column(db.String(5))
    documentNumber = db.Column(db.BigInteger())
    country = db.Column(db.String(40))
    department = db.Column(db.String(40))
    municipality = db.Column(db.String(40))
    firstName = db.Column(db.String(15))
    secondName = db.Column(db.String(15))
    firstLastName = db.Column(db.String(15))
    secondLastName = db.Column(db.String(15))
    address = db.Column(db.String(130))
    phone = db.Column(db.BigInteger())
    mail = db.Column(db.String(120))
    zipCode = db.Column(db.Integer())

    user = db.relationship('User', 
        backref= db.backref('user'))
    
    def __init__(self, user, documentType, documentNumber, country, department, municipality, firstName, secondName, firstLastName, secondLastName, address, phone, mail, zipCode):
        self.id_user = user['id']
        self.documentType = documentType
        self.documentNumber = documentNumber
        self.country = country
        self.department = department
        self.municipality = municipality
        self.firstName = firstName
        self.secondName = secondName
        self.firstLastName = firstLastName
        self.secondLastName = secondLastName
        self.address = address
        self.phone = phone
        self.mail = mail
        self.zipCode = zipCode

    def __repr__(self):
        return f'Supplier({self.documentNumber})'
        