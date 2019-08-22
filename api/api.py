import models
import os
import sys
import secrets
from PIL import Image, ImageChops

from flask import Blueprint, request, jsonify,url_for, send_file
from playhouse.shortcuts import model_to_dict
api = Blueprint('api', 'api', url_prefix="/api/v1")

def save_picture(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   picture_name = random_hex + f_ext
   file_path_for_avatar = os.path.join(os.getcwd(), 'static/shrub_pics/' + picture_name)
   output_size = (825, 825)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(file_path_for_avatar)
   return picture_name

@api.route('/', methods=["POST"])
def create_shrubs():
   print(request)
   print(type(request))
   pay_file = request.files
   payload = request.form.to_dict()
   dict_file = pay_file.to_dict()
   print(payload, '<-payload')
   print(dict_file, '<--dict_file')
   file_picture_path = save_picture(dict_file['file'])
   payload['image'] = file_picture_path
   print(payload, '<--payload', type(payload), 'type')
   shrub = models.Shrub.create(**payload)
   shrub_dict = model_to_dict(shrub)
   print(shrub.__dict__)
   return jsonify(data=shrub_dict, status={"code":201, "message":"success"})

@api.route('/', methods=["GET"])
def get_all_shrubs():
   try:
      shrubs = [model_to_dict(shrub) for shrub in models.Shrub.select()]
      return jsonify(data=shrubs, status={"code": 200, "message":"success"})
   except models.DoesNotExist:
      return jsonify(data={}, status={"code": 401, "message": "there was an error retrieving the resource"})

