from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    email           = db.Column(db.String(64), unique=True, index=True)
    password_hash   = db.Column(db.String(128))
    name            = db.Column(db.String(30))
    wishlist        = db.relationship('Wishlist', backref='user', lazy='dynamic')
    profile         = db.relationship('Profile', backref='profile', lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = db.session.query(User).get(data['id'])
        return user
    
    @property
    def is_authenticated(self):
        return True
    
    @property    
    def is_active(self):
        return True
        
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
    
    def __repr__(self):
        return '<User %r>' % self.email
        
        
class Wishlist(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    userid          = db.Column(db.Integer, db.ForeignKey('user.id'))
    itemUrl         = db.Column(db.String(250))
    imgUrl          = db.Column(db.String(250))
    title           = db.Column(db.String(60))
    description     = db.Column(db.String(500))
    
    def __repr__(self):
        return '<Item %r>' % self.title    

class Profile(db.Model):
    username    = db.Column(db.String(30),primary_key=True)
    userid      = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstname   = db.Column(db.String(30))
    lastname    = db.Column(db.String(30))
    image       = db.Column(db.String(30))
    sex         = db.Column(db.String(6))
    age         = db.Column(db.Integer)
    profile_added_on = db.Column(db.DateTime)

    def __repr__(self):
        return'<Profile %r>' % self.username