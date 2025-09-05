from config import api, app

from resources.User import UserList, User, BusinessList

from resources.Industry import IndustryList, Industry

from resources.BusinessIndustry import BusinessIndustryList, BusinessIndustry

from resources.BusinessHours import BusinessHoursList, BusinessHour

from resources.BusinessHourException import BusinessHourExceptionList, BusinessHourException

from resources.Prefectures import PrefectureList, Prefecture

from resources.Cities import CitiesList

from resources.Neighbourhoods import NeighbourhoodsList

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")
api.add_resource(BusinessList, "/businesses")

api.add_resource(IndustryList, "/industries")
api.add_resource(Industry, "/industries/<int:id>")

api.add_resource(BusinessIndustryList, "/businessindustires")
api.add_resource(BusinessIndustry, "/businessindustires/<int:id>")

api.add_resource(BusinessHoursList, "/businesshours")
api.add_resource(BusinessHour, "/businesshours/<int:id>")

api.add_resource(BusinessHourExceptionList, "/businesshoursexceptions")
api.add_resource(BusinessHourException, "/businesshoursexceptions/<int:id>")

api.add_resource(PrefectureList, "/prefectures")
api.add_resource(Prefecture, "/prefectures/<int:id>")

api.add_resource(CitiesList, "/cities")

api.add_resource(NeighbourhoodsList, "/neighbourhoods")

if __name__ == "__main__":
    app.run(port=5555, debug=True)