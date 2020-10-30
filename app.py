"""
Initialize your Flask app. This is what will run your server.

Don't forget to install your dependencies from requirements.txt!
This is a doc string! It's a special kind of comment that is expected
in Python files. Usually, you use this at the top of your code and in
every function & class to explain what the code does.
"""
from flask import Flask, render_template, request
from guests import Guest


# This code initializes a basic flask application.

app = Flask(__name__)

# Setting values to reference in the functions
my_name = "Veer"

halloween = "Saturday, October 31st"
spooky_time = "5:00pm"

guest_list = []


@app.route("/")
def homepage():
    """Return template for home."""

    return render_template("index.html", name=my_name)


@app.route("/about")
def aboutpage():
    return render_template("about.html", day=halloween, time=spooky_time)


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
