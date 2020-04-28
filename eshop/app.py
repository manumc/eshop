from datetime import date

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from eshop.metrics import Metrics

app = Flask(__name__)
api = Api(app)

metrics = Metrics()

@app.route("/")
def hello_world():
    return "Hello world!"

class Report(Resource):
    def get(self):
        request_date = request.args.get('date')

        try:
            valid_date = date.fromisoformat(request_date)
        except ValueError:
            return "Invalid query", 400
        except TypeError:
            return "Invalid parameter", 400

        return jsonify(metrics.create_report(valid_date))

api.add_resource(Report, '/api/v1/report')

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5050
    )
