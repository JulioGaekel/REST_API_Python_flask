from flask import Flask, jsonify, request

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()
