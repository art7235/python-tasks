from flask import Flask, request

app = Flask(__name__)

@app.route("/hello")
def home():
    return "Hello, world!"

@app.route("/hello/v2")
def hello():
    name = request.args.get("name")
    return {
        "message": f"Hello {name}"
    }

@app.route("/user")
def user():
    return {
        "name": "Andrey",
        "age": 17
    }

app.run()