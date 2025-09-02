from config import api, app

from resources.User import UserList, User

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)