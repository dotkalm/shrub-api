import models
import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify,url_for, send_file
from playhouse.shortcuts import model_to_dict
api = Blueprint('api', 'api', url_prefix="/api/v1")

def color_value(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   new_image = random_hex + f_ext
   file_path_for_pixel = os.path.join(os.getcwd(), 'static/one_pixel/' + new_image)
   output_size = (1, 1)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(file_path_for_pixel)
   pix = i.load()
   print(i.size,'<--- i.size!')
   rgb_values = pix[0,0]
   return rgb_values

def save_picture(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   picture_name = random_hex + f_ext
   file_path_for_avatar = os.path.join(os.getcwd(), 'static/shrub_pics/' + picture_name)
   output_size = (800, 800)
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
   pixel_picture_path = color_value(dict_file['file'])
   payload['average_red'] = pixel_picture_path[0]
   payload['average_green'] = pixel_picture_path[1]
   payload['average_blue'] = pixel_picture_path[2]
   payload['image'] = file_picture_path
   print(payload, '<--payload', type(payload), 'type')
   print(payload['average_green'])
   if payload['average_green'] > payload['average_red'] and payload['average_green'] > payload['average_blue']:
      print('mostly green')
      payload['detect_shrub'] = True
   else:
      print('hmm.. doesnt seem to be a shrub')
      payload['detect_shrub'] = False
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

@api.route('/<id>', methods=["DELETE"])
def delete_shrub(id):
    query = models.Shrub.delete().where(models.Shrub.id == id)
    query.execute()
    return jsonify(data="delete successful", status={"code": 200, "message":"resource succesfully deleted"})
