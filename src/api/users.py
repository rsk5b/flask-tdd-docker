# src/api/users.py


from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from src.api.crud import ( # isort:skip
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    add_user,
    update_user,
    delete_user
)

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user_fields = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @api.expect(user_fields, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email=email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        new_user = add_user(username=username, email=email)
        response_object["message"] = f"{email} was added!"
        return response_object, 201

    @api.marshal_with(user_fields, as_list=True)
    def get(self):
        users = get_all_users()
        return users


class Users(Resource):
    @api.marshal_with(user_fields)
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200

    def delete(self, user_id):
        response_object = {}
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        delete_user(user)
        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200

    @api.expect(user_fields, validate=True)
    def put(self, user_id):
        put_data = request.get_json()
        username = put_data.get("username")
        email = put_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        update_user(user, username, email)
        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<int:user_id>")
