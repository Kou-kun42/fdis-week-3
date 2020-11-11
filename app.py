"""
Initialize your Flask app. This is what will run your server.

Don't forget to install your dependencies from requirements.txt!
This is a doc string! It's a special kind of comment that is expected
in Python files. Usually, you use this at the top of your code and in
every function & class to explain what the code does.
"""
import os
import requests
from flask import Flask, render_template, request
from guests import Guest
from datetime import datetime, date
from pprint import PrettyPrinter


API_KEY = os.getenv("API_KEY")

# This initializes our PrettyPrinter object:
pp = PrettyPrinter(indent=4)

today = date.today()
# Now, let's just get the month as a number:
month = today.strftime('%m')
# Now, let's get the current year:
year = today.strftime('%Y')

# This code initializes a basic flask application.

app = Flask(__name__)

# Setting values to reference in the functions
my_name = "Veer"

halloween = "Saturday, October 31st"
spooky_time = "5:00pm"

guest_list = []


def get_holiday_data(result):
    """Loop through our JSON results and get only the information we need."""
    data = []
    for holiday in result["response"]["holidays"]:
        new_holiday = {
            "name": holiday["name"],
            "description": holiday["description"],
            "date": holiday["date"]["iso"],
        }
        data.append(new_holiday)
    return data


@app.route("/")
def homepage():
    """Return template for home."""

    return render_template("index.html", name=my_name)


@app.route('/about')
def about_page():
    """Show user party information."""
    # Sometimes, a cleaner way to pass variables to templates is to create a
    # context dictionary, and then pass the data in by dictionary key

    url = 'https://calendarific.com/api/v2/holidays'

    params = {
        "api_key": API_KEY,
        "country": "US",
        "year": year,
        "month": month
    }

    result_json = requests.get(url, params=params).json()
    # pp.pprint(result_json)

    data = get_holiday_data(result_json)
    holidays = []
    dates = []
    descriptions = []

    for holiday in data:
        holidays.append(holiday["name"])
        dates.append(holiday["date"])
        descriptions.append(holiday["description"])

    context = {
        "holidays": holidays,
        "dates": dates,
        "descriptions": descriptions
    }

    return render_template('about.html', **context)


@app.route("/guests", methods=["GET", "POST"])
def guestspage():
    if request.method == "GET":
        return render_template("guests.html", guests=guest_list)
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        costume = request.form.get("costume")
        coming = request.form.get("coming")
        guest_list.append(Guest(name, email, plus_one, phone, costume, coming))
        return render_template("guests.html", guests=guest_list)


@app.route("/rsvp")
def rsvppage():
    return render_template("rsvp.html", guests=guest_list)


if __name__ == "__main__":
    app.run(debug=True)
