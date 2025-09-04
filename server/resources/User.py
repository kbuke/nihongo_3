from models.User import UserModel, AdminModel, TravelerModel, BusinessModel
from flask import request, make_response, session
from flask_restful import Resource
from config import db

class UserList(Resource):
    # Get all users
    def get(self):
        users = [user.to_dict(rules = (
            "-_password_hash",
            "-hour_exceptions",
            "-hours",
        )) for user in UserModel.query.all()]
        return users

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
                        ac_type = ac_type,
                        name = json.get("name"),
                        nationality = json.get("nationality")
                    )
                    new_user.password_hash=json.get("newPassword")
                    db.session.add(new_user)
                    db.session.commit()
                    return {"message": "Created account!"}
                
                elif ac_type == "Traveler":
                    new_traveler = TravelerModel(
                        email = json.get("email"),
                        picture = json.get("picture"),
                        intro = json.get("intro"),
                        ac_type = ac_type,
                        name = json.get("name"),
                        nationality = json.get("nationality")
                    )
                    new_traveler.password_hash=json.get("newPassword")
                    db.session.add(new_traveler)
                    db.session.commit()
                    return {"message": "New traveler added"}
                
                elif ac_type == "Business":
                    new_business = BusinessModel(
                        email = json.get("email"),
                        picture = json.get("picture"),
                        intro = json.get("intro"),
                        ac_type = ac_type,
                        business_name = json.get("businessName"),
                        open_24hr = json.get("24hr"),
                        allow_email = json.get("allowEmail"),
                        chome = json.get("chome"),
                        block = json.get("block"),
                        building_number = json.get("buildingNumber"),
                        building_name = json.get("buildingName"),
                        floor = json.get("floor"),
                        room = json.get("room"),
                        post_code = json.get("postCode")
                    )
                    new_business.password_hash=json.get("newPassword")
                    db.session.add(new_business)
                    db.session.commit()
                    return {"message": "New business added"}
                
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": "Failed to add new user"}

class User(Resource):
    # Get specific user
    def get(self, id):
        user = UserModel.query.filter(UserModel.id==id).first()
        if user:
            return user.to_dict(), 201
        else:
            return{"error": f"User {id} not found"}
    
    # PATCH specific user info
    def patch(self, id):
        data = request.get_json()

        user = UserModel.query.filter(UserModel.id==id).first()
        if user:
            try:
                for attr in data:
                    setattr(user, attr, data[attr])
                db.session.add(user)
                db.session.commit()
                return {"message": f"User {id} updated."}
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return{"error": "Message not found"}

    def delete(self, id):
        user = UserModel.query.filter(UserModel.id==id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {id} deleted!"}
        else:
            return {"error": f"User {id} not found"}, 404
        
class BusinessList(Resource):
    def get(self):
        businesses = [business.to_dict() for business in BusinessModel.query.all()]
        return businesses, 201
