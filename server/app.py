from config import api, app

from resources.User import UserList, User, BusinessList

from resources.Industry import IndustryList, Industry

from resources.BusinessIndustry import BusinessIndustryList

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")
api.add_resource(BusinessList, "/businesses")

api.add_resource(IndustryList, "/industries")
api.add_resource(Industry, "/industries/<int:id>")

api.add_resource(BusinessIndustryList, "/businessindustires")

if __name__ == "__main__":
    app.run(port=5555, debug=True)