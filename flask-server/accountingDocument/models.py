from application import db, BaseModelMixin

class AccountingDocument(db.Model, BaseModelMixin):

    id = db.Column(db.Integer(), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date(),default=0)
    description = db.Column(db.String(150))
    consecutive= db.Column(db.Integer())
    prefix = db.Column(db.String(5))
    documentType = db.Column(db.String(15))
    template = db.Column(db.String(15))
    
    user = db.relationship('User', 
        backref= db.backref('user'))
    
    def __init__(self, user, date, description, consecutive, prefix, documentType, template):
        self.id_user = user['id']
        self.date = date
        self.description = description
        self.consecutive = consecutive
        self.prefix = prefix
        self.documentType = documentType
        self.template = template

    def __repr__(self):
        return f'Accounting Document ({self.description})'
    
    
        