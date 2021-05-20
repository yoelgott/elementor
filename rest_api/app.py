from flask import Flask, request
from flask_restful import Resource, Api
from sites_handler import SitesHandler

app = Flask(__name__)
api = Api(app)


class Elementor(Resource):
    def post(self):
        json_data = request.get_json()
        sites = json_data.get("sites")
        if isinstance(sites, str):
            sites = [sites]
        sites_assest = SitesHandler(sites).run()
        return {"sites_assessment": sites_assest}


api.add_resource(Elementor, "/assest-sites")

if __name__ == "__main__":
    app.run(debug=True)
