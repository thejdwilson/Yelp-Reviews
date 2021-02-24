# You will need to first run "pip install requests" in your venv
from secrets import *
from flask import Flask, json, request
import requests

app = Flask(__name__)


def get_response(business_id):
    uri = 'https://api.yelp.com/v3/businesses/' + business_id + '/reviews'
    return requests.get(uri, headers={'Authorization': 'Bearer ' + bearer_token})


def get_reviews(response):
    response_data = response.json()
    data = []
    for review in response_data["reviews"]:
        data.append({"review_id": review["id"],
                     "review_text": review["text"],
                     "user_id": review["user"]["id"],
                     "profile_url": review["user"]["profile_url"]})
    return data


@app.route("/reviews", methods=["GET"])
def main():
    try:
        restaurant = request.args.get("id")
        response = get_response(restaurant)
        restaurant_data = get_reviews(response)
        return json.dumps(restaurant_data, sort_keys=True, indent=4)
    except KeyError:
        return "Restaurant not found"


if __name__ == "__main__":
    app.run()
