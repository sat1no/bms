from __init__ import db


class Moduly(db.Model):
    __tablename__ = 'Moduly'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100)) 


    urzadzenia = db.relationship('Urzadzenia', backref = 'urzadzenia', lazy = 'dynamic')
    
    # def __init__(self, name, value1):
    #     self.name = name
    #     self.value1 = value1

        
class Urzadzenia(db.Model):
    __tablename__ = 'Urzadzenia'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column('nazwa', db.String(100) )
    rejestr = db.Column('rejestr', db.Integer, nullable=False)
    sterowanie = db.Column('sterowanie', db.String(100))
    stan = db.Column('stan', db.Integer)
    wartosc = db.Column('wartosc', db.Integer)
    r = db.Column('r', db.Integer)
    g= db.Column('g', db.Integer)
    b = db.Column('b', db.Integer)
    modul_id = db.Column(db.Integer, db.ForeignKey('Moduly.id'))
    
    
    

 
    

        
        
