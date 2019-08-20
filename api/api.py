import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
api = Blueprint('api', 'api', url_prefix="/api/v1")

@api.route('/', methods=["POST"])
def create_shrubs():
   payload = request.get_json()
   print(payload, '<--payload', type(payload), 'type')
   shrub = models.Shrub.create(**payload)
   shrub_dict = model_to_dict(shrub)
   print(shrub.__dict__)
   return jsonify(data=shrub_dict, status={"code":201, "message":"success"})