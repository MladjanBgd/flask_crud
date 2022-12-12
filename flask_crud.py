# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 08:54:18 2022

@author: mladjan.jovanovic
"""

import os
from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "database.sqlite"
)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    """
    Class User where we store username and email
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<username: %s, email: %s>' %(self.username, self.email)

class UserSchema(ma.Schema):
    """
    User Schema for de/serialistaion json
    """
    username = fields.String(required=True, allow_none=True)
    email = fields.Email(required=True, allow_none=True)
    
    class Meta:
        fileds = ("username", "email")  # fields to expose


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/user", methods=["POST"], strict_slashes=False)
def add_user():
    """
    endpoint for add user
    """
    username = request.json["username"]
    email = request.json["email"]
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    result = user_schema.dump(new_user)
    return result, 201

@app.route("/user", methods=["GET"])
def user_list():
    """
    endpoint for show all user
    """
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return result, 201

@app.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    """
    endpoint for show user
    """
    user_id = User.query.get(id)

    result = user_schema.dump(user_id)
    return result, 201

@app.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    """
    endpoint for update user
    """
    username = request.json["username"]
    email = request.json["email"]

    user = User.query.get(id)
    user.username = username
    user.email = email

    db.session.commit()

    #return user_schema.jsonify(user)
    result = user_schema.dump(user)
    return result, 201

@app.route("/user/<int:id>", methods=["DELETE"], strict_slashes=True)
def delete_user(id):
    """
    endpoint for delete user
    """
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"sucess:": "True"})


#playing with RESTfull
from flask_restful import Resource, Api
api = Api(app)
class Hi(Resource):
    def get(self):
        return {'hello': 'world'}
api.add_resource(Hi, '/')

if __name__ == "__main__":
    app.run(debug=True)
    
#prepare database    
# from flask_crud import db, app
# with app.app_context():
#     db.create_all()


#{"username":"Najnoviji User","email":"new222@blah.com"}
#curl to add user
#curl -i -H "Content-Type: application/json" -X POST -d "{\"username\":\"abc\", \"email\":\"abc@blob.com\"}" "http://127.0.0.1:5000/user"