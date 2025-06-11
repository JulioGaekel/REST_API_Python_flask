from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)
# Configure where the database file will be. By creating the basedir variable and using the os library, the location has been set to the same location as the app.py file (current project).
basedir = os.path.abspath(os.path.dirname(__file__))

# Set up configuration manager included in flask. Config key has to match 'SQLALCHEMY_DATABASE_URI'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "planets.db")

# Initialize the database, this must be done before actually using it.
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the planetary API.'), 200

@app.route("/not_found")
def not_found():
    return jsonify(message="The resource you are trying to reach was not found."), 404

# To use this parameters route with request arguments, the URL should look like this http://127.0.0.1:5000/parameters?name=Bruce&age=28. Notice after the route, there is no forward slash but a question mark with the name variable and our String. To test the parameters route use Postman.
@app.route("/parameters")
def parameters():
    name = request.args.get("name")
    age = int(request.args.get("age"))
    if age <= 18:
        return jsonify(message="Sorry " + name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough."), 200

@app.route("/url_variables/<string:name>/<int:age>")
def url_variables(name: str, age: int):
    if age <= 18:
        return jsonify(message="Sorry " + name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough."), 200


# DATABASE MODELS
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = "planets"
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == '__main__':
    app.run()
