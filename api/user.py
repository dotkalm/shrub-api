import models 

import os
import sys
import secrets

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   picture_name = random_hex + f_ext
   file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)
   output_size = (125, 175)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(file_path_for_avatar)
   return picture_name

@user.route('/register', methods=["POST"])
def register():
    print(request)
    print(type(request))
   #  pay_file = request.files
    payload = request.form.to_dict()
   #  dict_file = pay_file.to_dict()
    print(payload)
    user = models.User.create(**payload) 
    print(type(user)) 
    login_user(user) 
    user_dict = model_to_dict(user)
    print(user_dict)
    print(type(user_dict))
    return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login/', methods=["POST"])
def login():
   print(request)
   print(type(request))
   # payload = request.form.to_dict()
   payload = request.get_json()
   print(payload)
   user = models.User.get(models.User.username == payload['username'])
   user_dict = model_to_dict(user)
   print(user_dict)

   return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

      