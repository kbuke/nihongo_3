from models.User import UserModel, AdminModel
from flask import request, make_response, session
from flask_restful import Resource
from config import db

class UserList(Resource):
    # Create a new user
    def post(self):
        json = request.get_json()

        if json:
            ac_type = json.get("acType")
            try:
                if ac_type == "Admin":
                    new_user = AdminModel(
                        email = json.get("email"),
                        picture = json.get("profilePicture"),
                        intro = json.get("intro"),
                        ac_type = json.get("acType"),
                        name = json.get("name"),
                        nationality = json.get("nationality")
                    )
                    new_user.password_hash=json.get("newPassword")
                    db.session.add(new_user)
                    db.session.commit()
                    return {"message": "Created account!"}
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": "Failed to add new user"}

class User(Resource):
    def delete(self, id):
        user = UserModel.query.filter(UserModel.id==id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {id} deleted!"}
        else:
            return {"error": f"User {id} not found"}, 404
