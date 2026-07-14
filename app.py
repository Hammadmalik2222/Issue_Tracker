from flask import Flask                             # import class
from flask import render_template                   # render & return html file

app = Flask(__name__)                               # instance of class


@app.route("/")                                     # root U
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)