from db import db


class Property(db.Model):
    """
  This class represents a property in the database.
  """
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    num_bedrooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    location = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    property_type = db.Column(db.String(80))
    price = db.Column(db.Integer)

    def __init__(self, new_property):
        self.title = new_property['title']
        self.description = new_property['description']
        self.num_bedrooms = new_property['num_bedrooms']
        self.num_bathrooms = new_property['num_bathrooms']
        self.location = new_property['location']
        self.photo = new_property['photo']
        self.property_type = new_property['property_type']
        self.price = new_property['price']

    def __repr__(self):
        return f'<Property {self.id} - {self.title}>'
