from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    serialize_rules = ('-reviews.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    #Customer has many reviews
    reviews = db.relationship('Review', back_populates='customer', cascade="all, delete-orphan")

    #to get a list of items a customer has reviewed , add association proxy => thru customer's reviews relationship.
    items = association_proxy('reviews', 'item', creator=lambda item_obj: Review(item=item_obj))

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    serialize_rules = ('-reviews.item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    #item has many reviews
    reviews = db.relationship('Review', back_populates='item')


    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    

# Review is association table(JOIN)
# A review belongs to a customer.
# A review belongs to an item.
# A customer has many items through reviews.
# An item has many customers through reviews.
class Review(db.Model, SerializerMixin):  # 2nd migration for this table

    __tablename__ = 'reviews'

    serialize_rules = ('-customer.reviews', '-item.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    #Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id')) #points to pk of customers table. 
    item_id = db.Column(db.Integer, db.ForeignKey('items.id')) # points to pk of items table.

    # A review belongs to a customer.
    customer = db.relationship('Customer', back_populates='reviews')

    # review belongs to an item.
    item = db.relationship('Item', back_populates='reviews')
