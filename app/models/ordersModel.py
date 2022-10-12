from marshmallow import fields, Schema, validate
from . import db
from .productsModel import ProductSchema
class OrdersModel(db.Model):
    
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(60))
    status= db.Column(db.String(60))
    products = db.relationship("ProductsModel", backref='products')

    def __init__(self,data):
        """
        Class constructor
        """
        self.name= data.get('name')
        self.status = data.get('status')
    

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
    def get_all_orders():
        return OrdersModel.query.all()

    @staticmethod
    def get_one_order(id):
        return OrdersModel.query.get(id)

    @staticmethod
    def get_order_by_nombre(value):
        return OrdersModel.query.filter_by(nombre=value).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def all_paginated(jsonFilter, page=1, per_page=10):
        return OrdersModel.query.filter_by(**jsonFilter).order_by(OrdersModel.id.asc()).paginate(page=page, per_page=per_page, error_out=False)

class OrderSchema(Schema):
    """
    Order Schema
    """
    id = fields.Int()
    name= fields.Str(required=True, validate=[validate.Length(max=60)])
    status=fields.Str()
    products= fields.Nested(ProductSchema, many=True)
class QuerySchemaFilter(Schema):
    status=fields.Str()

class QueryOrderSchema(Schema):
    filter = fields.Nested(QuerySchemaFilter)
    bloques =fields.Str()