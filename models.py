from app import db

class UserModel(db.Model):
    __tablename__ = 'user'
    
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    
    def __init__(self, name, email, password):
        # self.userId = userId
        self.name = name
        self.email = email
        self.password = password
    
    def to_dict(self):
        return {
            'userId': self.userId,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

class PropertyModel(db.Model):
    __tablename__ = 'property'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    amenities = db.Column(db.ARRAY(db.String), nullable=True)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    def __init__(self, title, amenities, price, location):
        self.title = title
        self.amenities = amenities
        self.price = price
        self.location = location
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amenities': self.amenities,
            'price': self.price,
            'location': self.location
        }