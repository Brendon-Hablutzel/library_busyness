from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

CORS(app)


class Predict(Resource):
    def get(self):
        res = {
            "predictions": {
                "2024-04-01T23:03": {
                    "hill": {
                        "total": 300
                    },
                    "hunt": {
                        "total": 200
                    }
                }
            }
        }
        return res, 200


api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    app.run()
