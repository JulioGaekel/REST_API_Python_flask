from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from marshmallow import fields


# ------------------------------------------ APP CONFIG SETUP -----------------------------------------
app = Flask(__name__)
# Configure where the database file will be. By creating the basedir variable and using the os library, the location has been set to the same location as the app.py file (current project).
basedir = os.path.abspath(os.path.dirname(__file__))

# Set up configuration manager included in flask. Config key has to match 'SQLALCHEMY_DATABASE_URI'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "planets.db")

# Initialize the database, this must be done before actually using it.
db = SQLAlchemy(app)
ma = Marshmallow(app)

# ---------------------------------------- END APP CONFIG SETUP ----------------------------------------


# Create a command using a decorator to create the database.
@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created!")


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Database dropped!")


@app.cli.command("db_seed")
def db_seed():
    mercury = Planet(planet_name="Mercury",
                     planet_type="Class D",
                     home_star="Sol",
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name="Venus",
                     planet_type="Class K",
                     home_star="Sol",
                     mass=4.867e24,
                     radius=3760,
                     distance=67.24e6)

    earth = Planet(planet_name="Earth",
                     planet_type="Class M",
                     home_star="Sol",
                     mass=5.972e24,
                     radius=3959,
                     distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name = "William",
                     last_name = "Herschel",
                     email = "test@test.com",
                     password = "p@ssword")

    db.session.add(test_user)
    db.session.commit()
    print("Database seeded.")

# ---------------------------------------------- ROUTES --------------------------------------------
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


@app.route("/planets", methods=["GET"])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@app.route("/register", methods=['POST'])
def register():
    email = request.form["email"]
    test = User.query.filter_by(email=email).first()

    if test:
        return jsonify(message="That email already exists."), 409
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201
# ---------------------------------------------- END ROUTES --------------------------------------------


# ------------------------------------------- DATABASE MODELS ------------------------------------------
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

class UserSchema(ma.Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    password = fields.Str()

class PlanetSchema(ma.Schema):
    planet_id = fields.Int()
    planet_name = fields.Str()
    plant_type = fields.Str()
    home_star = fields.Str()
    mass = fields.Float()
    radius = fields.Float()
    distance = fields.Float()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)


if __name__ == '__main__':
    app.run()
