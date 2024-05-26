import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return { "message": "Store deleted." }
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(201, StoreSchema(many=True))
    def get(self):
        return list(stores.values())

    @blp.arguments(StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists")
        store_id = uuid.uuid4().hex
        new_store = { **store_data, "id": store_id }
        stores[store_id] = new_store
        return new_store, 201


