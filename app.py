# The "secrets" file contains the bearer_token value. You will need to supply your own if you wish to run this locally
from secrets import *
from flask import Flask, json, request
import requests

app = Flask(__name__)


def get_location(uri):
    business_data = requests.get(uri, headers={'Authorization': 'Bearer ' + bearer_token}).json()
    return business_data["location"]["display_address"]


def get_reviews(uri):
    reviews = requests.get(uri + "/reviews", headers={'Authorization': 'Bearer ' + bearer_token}).json()
    return reviews["reviews"]


def get_review_details(location, reviews):
    data = []
    for review in reviews:
        data.append({"user_name": review["user"]["name"],
                     "avatar_image_url": review["user"]["image_url"],
                     "location": location,
                     "rating": review["rating"],
                     "review_content": review["text"]})
    return data


@app.route("/reviews", methods=["GET"])
def main():
    try:
        restaurant_id = request.args.get("id")
        uri = 'https://api.yelp.com/v3/businesses/' + restaurant_id
        location = get_location(uri)
        reviews = get_reviews(uri)
        restaurant_data = get_review_details(location, reviews)
        return json.dumps(restaurant_data, sort_keys=False, indent=4)
    except KeyError:
        return "Restaurant not found"


if __name__ == "__main__":
    app.run()
