from marshmallow import fields, Schema, validate
from . import db

class ProductsModel(db.Model):
    
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(60))
    skus= db.Column(db.String(60))
    quantity = db.Column(db.Integer) 
    Idorders = db.Column( db.Integer, db.ForeignKey("orders.id"))


    def __init__(self,data):
        """
        Class constructor
        """
        self.name= data.get('name')
        self.skus= data.get('skus')
        self.quantity = data.get('quantity')
        self.Idorders = data.get('Idorders')
    

    # POST PARA CREAR ALGO EN LA DB
    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        return self.id

    # PARA ACTUALIZAR ALGO EN LA DB
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    #PARA BORRAR ALGO EN LA DB
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_products():
        return ProductsModel.query.all()

    @staticmethod
    def get_one_product(id):
        return ProductsModel.query.get(id)

    @staticmethod
    def get_product_by_sku(value):
        return ProductsModel.query.filter_by(skus=value).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

class ProductSchema(Schema):
    """
    Product Schema
    """
    id = fields.Int()
    name= fields.Str(required=True, validate=[validate.Length(max=60)])
    skus= fields.Str(required=True)
    quantity = fields.Int()
    Idorders = fields.Int(required=True)