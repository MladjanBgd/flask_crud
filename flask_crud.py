# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 08:54:18 2022

@author: mladjan.jovanovic
"""

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "databse.sqlite"
)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    """
    Class User where we store username and email
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    """
    User Schema for de/serialistaion json
    """

    class Meta:
        fileds = ("username", "email")  # fields to expose


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/user", method=["POST"])
def add_user():
    """
    endpoint for add user
    """
    username = request.json["username"]
    email = request.json["email"]
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


@app.route("user", method=["GET"])
def user_list():
    """
    endpoint for show all user
    """
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result.data)


@app.route("/user/<id>", method=["GET"])
def get_user(id):
    """
    endpoint for show user
    """
    user_id = User.query.get(id)

    return user_schema.jsonify(user_id)


@app.route("user/<id>", method=["PUT"])
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

    return user_schema.jsonify(user)


@app.route("user/<id>", method=["DELETE"])
def delete_user(id):
    """
    endpoint for delete user
    """
    user = User.query.get(id)

    db.session.delete(id)
    db.commit()

    return user_schema.jsonify(user)


if __name__ == "__main__":
    app.run(debug=True)
