from __init__ import db

# class User(db.Model):
#     
#     # followers = db.Table('followers',
#     # db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     # db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))
#     
#     id = db.Column(db.Integer, primary_key = True)
#     nickname = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     modul = db.relationship('Moduly', backref = 'creator', lazy = 'dynamic')
#     # followed = db.relationship('User', 
#     #                            secondary=followers, 
#     #                            primaryjoin=(followers.c.follower_id == id), 
#     #                            secondaryjoin=(followers.c.followed_id == id), 
#     #                            backref=db.backref('followers', lazy='dynamic'), 
#     #                            lazy='dynamic')
#     
# 
#     
#     def follow(self, user):
#         if not self.is_following(user):
#             self.followed.append(user)
#             return self
# 
#     def unfollow(self, user):
#         if self.is_following(user):
#             self.followed.remove(user)
#             return self
# 
#     def is_following(self, user):
#         return self.followed.filter(followers.c.followed_id == user.id).count() > 0
#     def __repr__(self):
#         return '<User %r>' % (self.nickname)
    
    
# class Modul(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(64))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     
#     def __repr__(self):
#         return '<Modul %r>' % (self.name)


class Moduly(db.Model):
    __tablename__ = 'Moduly'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    value1 = db.Column(db.Integer)  


    urzadzenia = db.relationship('Urzadzenia', backref = 'urzadzenia', lazy = 'dynamic')
    
    # def __init__(self, name, value1):
    #     self.name = name
    #     self.value1 = value1

        
class Urzadzenia(db.Model):
    __tablename__ = 'Urzadzenia'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column('nazwa', db.String(100) )
    rejestr = db.Column('rejestr', db.Integer, unique=True, nullable=False)
    sterowanie = db.Column('sterowanie', db.String(100))
    wartosc = db.Column('wartosc', db.Integer)
    r = db.Column('r', db.Integer)
    g= db.Column('g', db.Integer)
    b = db.Column('b', db.Integer)
    modul_id = db.Column(db.Integer, db.ForeignKey('Moduly.id'))
    
    
    

 
    

        
        
