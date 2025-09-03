from config import api, app

from resources.User import UserList, User

from resources.BusinessType import BusinessTypeList, Business

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")

api.add_resource(BusinessTypeList, "/businesstypes")
api.add_resource(Business, "/businesstypes/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)