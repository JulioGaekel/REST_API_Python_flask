from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the planetary API.')


@app.route("/parameters")
def parameters():
    name = request.args.get("name")
    age = int(request.args.get("age"))
    if age <= 18:
        return jsonify(message = "Sorry " + name + ", you are not old enough")

if __name__ == '__main__':
    app.run()
