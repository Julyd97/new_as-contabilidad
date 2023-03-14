from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80))
    telephone = db.Column(db.BigInteger())
    email = db.Column(db.String(120))
    password = db.Column(db.String(128))
    college_name = db.Column(db.String(80))
    college_direction = db.Column(db.String(120))
    college_nit = db.Column(db.Integer())
    

    def __init__(self, full_name, telephone, email, password, college_name, college_direction, college_nit):
        self.full_name = full_name
        self.telephone = telephone
        self.email = email
        self.password = password
        self.college_name = college_name
        self.college_direction = college_direction
        self.college_nit = college_nit
    
    def __repr__(self):
        return '<User %r>' %self.full_name