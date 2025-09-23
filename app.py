from flask import Flask, request

app = Flask(__name__)

animals = ["Zebra", "Lejon", "Fisk", "Struts"]


@app.route("/")
def index():
    return animals


if __name__ == "__main__":
    app.run(debug=True, port=4001)
