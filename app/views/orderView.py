from flask import Flask,request,json
from flask_restx import Api,fields,Resource, Namespace
from ..models.ordersModel import OrdersModel,OrderSchema,QueryOrderSchema
from ..models import db

app = Flask(__name__)

nsOrder= Namespace("Orders", description="Endpoint operations for Orders")
order_schema = OrderSchema()
query_schema_orders_filter = QueryOrderSchema()
OrderModelApi = nsOrder.model(
    "OrderModel",
    {
        "name": fields.String(required=True, description="name"),
        "status": fields.String(description="status"),
    }
)
OrderModelApiFilter = nsOrder.model(
    "OrderModelFilter",
    {
        "status": fields.String(description="status"),
    }
)
OrderModelListApi = nsOrder.model('OrderList', {
    'orders': fields.List(fields.Nested(OrderModelApi)),
})

orderPatchApi = nsOrder.model(
    "OrderPatchModel",
    {
        
        "id": fields.Integer(required=True, description="identificador"),
        "name": fields.String(required=True, description="name"),
        "status": fields.String(description="status"),
        
    }
)

orderQueryApi = nsOrder.model(
    "OrderQueryModelFilter",
    {
        "filter": fields.Nested(OrderModelApiFilter),
    }
)

##### FUNCTION FOR CREATE ORDERS
def createOrder(req_data, listaObjetosCreados):
    app.logger.info("Creando inserts" + json.dumps(req_data))
    data = None
    try:
        data = order_schema .load(req_data)
    except:
        return json.dumps('error in the formation of json'),400

    order = OrdersModel(data)
    print(order)
    try:
        order.save()
    except:
        print('errores')
    
    serialized_order = order_schema.dump(order)
    listaObjetosCreados.append(serialized_order)
    
###################################


@nsOrder.route("")
class OrderList(Resource):

    ######## GET ALL ORDERS
    @nsOrder.doc("Read orders")
    def get(self):
        """List all Orders"""
        orders = OrdersModel.get_all_orders()
        serialized_orders = order_schema.dump(orders, many=True)
        return serialized_orders,200
    
    ###########################
    
    ######CREATE ALL ORDERS
    @nsOrder.doc("Crete Orders")
    @nsOrder.expect(OrderModelListApi)
    @nsOrder.response(201, "created")
    def post(self):
        """Crete Orders"""
        req_data = request.get_json().get("orders")
        if(not req_data):
            return json.dumps('error there is not data'),404
        try:
            data = order_schema.load(req_data, many=True)
        except :
            return json.dumps('error in the formation of json'),400
        
        listaObjetosCreados = list()
        
        for dataItem in data:
            createOrder(dataItem, listaObjetosCreados)
        
  
        return listaObjetosCreados,201
    #################################


   
    ######### UPDATE ONE ORDER#######
    @nsOrder.doc("Update one Order")
    @nsOrder.expect(orderPatchApi)
    def patch(self):
        """Update one Order"""
        req_data = request.get_json()
        data = None
        try:
            data = order_schema.load(req_data, partial=True)
        except :
            return json.dumps('error in the formation of json'),400

        order = OrdersModel.get_one_order(data.get("id"))
        if not order:
            return json.dumps('error there is not order'),404

        try:
            order.update(data)
        except Exception as err:
            return json.dumps('error the update'),400

        serialized_order = order_schema.dump(order)
        return serialized_order,200
    ##########################################

##############DELETE ONE ORDER
@nsOrder.route("/<id>")
@nsOrder.param("id", "The id identifier")
@nsOrder.response(404, "registro no encontrado")
class OneOrder(Resource):
    @nsOrder.doc("delete order")
    def delete(self, id):
        """Delete one Order"""
        order = OrdersModel.get_one_order(id)
        print(order)
        if not order:
            return print('error no hay order'),404

        try:
           order.delete()
        except Exception as err:
            return print('error al actualizar'),400

        serialized_order = order_schema.dump(order)
        return serialized_order
###############################

###########FILTER X STATUS AND PAGINATE 
@nsOrder.route("/<int:page>/<int:per_page>")
@nsOrder.param("status", "The status manage")
@nsOrder.expect(orderQueryApi)
@nsOrder.response(404, "order not found")
class PaginateOrderFilter(Resource):
    @nsOrder.doc("Get order for filter")
    def post(self, page, per_page):
        """
            Query based in filter dynamic and paginate
        """
        jsonData= request.json
        print(jsonData)
        try:
            query_schema_orders_filter.load(jsonData)
        except :
            return json.dumps('error in the formation of json'),400

        jsonFilter = jsonData["filter"]
        orders= OrdersModel.all_paginated(jsonFilter, page, per_page)
        print(orders)
        data= order_schema.dump(orders.items, many=True)
        return data,200
###############################