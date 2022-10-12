from flask import Flask,json,request
from flask_restx import Api,fields,Resource, Namespace
from ..models.productsModel import ProductsModel,ProductSchema
from ..models import db

app = Flask(__name__)

nsProduct= Namespace("Products", description="Endpoint operations for Products")
product_schema = ProductSchema()
ProductModelApi = nsProduct.model(
    "ProductModel",
    {
        "name": fields.String(required=True, description="name"),
        "skus": fields.String(description="skus"),
        "quantity": fields.Integer(description="quantity"),
        "Idorders": fields.Integer(required=True,description="Idorders")
    }
)

ProductModelListApi = nsProduct.model('ProductList', {
    'products': fields.List(fields.Nested(ProductModelApi)),
})

productPatchApi = nsProduct .model(
    "ProductPatchModel",
    {
        
        "id": fields.Integer(required=True, description="identificador"),
        "skus": fields.String(description="skus"),
        "quantity": fields.Integer(description="quantity"),
        "Idorders": fields.Integer(required=True,description="Idorders")
        
    }
)

##### FUNCTION FOR CREATE LIST OF PRODUCTS
def createProduct(req_data, listaObjetosCreados, listaerrores):
    app.logger.info("Creando inserts" + json.dumps(req_data))
    data = None
    try:
        data = product_schema.load(req_data)
    except:
        return json.dumps('error in the formation of json'),400

    # Validate for if Skus the product already exists
    product_in_db_sku = ProductsModel.get_product_by_sku(data.get("skus"))
    print(product_in_db_sku)
    if product_in_db_sku:
          error = "Producto con Sku duplicado"
          listaerrores.append(error )

    else:
        Product = ProductsModel(data)
        print(Product)
        try:
            Product.save()
        except:
            print('errores')
        
        serialized_Product = product_schema.dump(Product)
        listaObjetosCreados.append(serialized_Product)
##################################    

@nsProduct.route("")
class ProductList(Resource):
    ######## GET ALL PRODUCTS
    @nsProduct.doc("Read Products")
    def get(self):
        """List all Products"""
        Products = ProductsModel.get_all_products()
        serialized_Products = product_schema.dump(Products, many=True)
        return serialized_Products,200
    ##########################

    ######CREATE ALL PRODUCTS
    @nsProduct.doc("Crete Products")
    @nsProduct.expect(ProductModelListApi)
    @nsProduct.response(201, "created")
    def post(self):
        """Crete Products"""
        req_data = request.get_json().get("products")
        if(not req_data):
            return json.dumps('error'),404
        try:
            data = product_schema.load(req_data, many=True)
        except :
            return json.dumps('error in the formation of json'),400
        
        listaObjetosCreados = list()
        listaerrores = list()
        for dataItem in data:
            createProduct(dataItem, listaObjetosCreados, listaerrores)
        
        if (len(listaObjetosCreados) > 0):
            if(len(listaerrores)== 0):
                return listaObjetosCreados,201
  
        else:
            return (listaerrores)
    ################################
    
    ######### UPDATE ONE PRODUCT#######
    @nsProduct.doc("actualizar Product")
    @nsProduct.expect(productPatchApi)
    def patch(self):
        """Update one Product"""
        req_data = request.get_json()
        data = None
        try:
            data = product_schema.load(req_data, partial=True)
        except :
            return json.dumps('error in the formation of json'),400

        Product = ProductsModel.get_one_product(data.get("id"))
        if not Product:
            return json.dumps('error no hay Product'),404
        
        try:
            Product.update(data)
        except Exception as err:
            return json.dumps('error al actualizar'),400

        serialized_Product = product_schema.dump(Product)
        return serialized_Product,200
    ##########################################

##############DELETE ONE PRODUCT
@nsProduct.route("/<id>")
@nsProduct.param("id", "The id identifier")
@nsProduct.response(404, "registro no encontrado")
class OneProduct(Resource):
    @nsProduct.doc("delete Product")
    def delete(self, id):
        """Delete one Product"""
        Product = ProductsModel.get_one_product(id)
        print(Product)
        if not Product:
            return json.dumps('error no hay Product'),404

        try:
           Product.delete()
        except Exception as err:
            return json.dumps('error al actualizar'),400

        serialized_Product = product_schema.dump(Product)
        return serialized_Product
###############################
