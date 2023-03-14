from application import db, BaseModelMixin

class Account(db.Model, BaseModelMixin):

    id = db.Column(db.Integer(), primary_key=True)
    id_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer(), nullable = True)
    level = db.Column(db.String(2))
    serial = db.Column(db.String(20))
    description = db.Column(db.String(150))
    portfolio = db.Column(db.Boolean())
    stakeholder = db.Column(db.Boolean())
    supplier = db.Column(db.Boolean())
    costCenter = db.Column(db.Boolean())
    nature = db.Column(db.Boolean())
    type = db.Column(db.String(15))

    user = db.relationship('User', 
        backref= db.backref('user'))

    def __init__(self, user, parent_id, level, serial, description, portfolio, stakeholder, supplier, costCenter, nature, type):
        self.id_user = user['id']
        self.parent_id = parent_id
        self.level = level
        self.serial = serial
        self.description = description
        self.portfolio = portfolio
        self.stakeholder = stakeholder
        self.supplier = supplier
        self.costCenter = costCenter
        self.nature = nature
        self.type = type
    
    def __repr__(self):
        return self.serial