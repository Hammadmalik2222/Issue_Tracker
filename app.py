from flask import Flask                             # import class
from flask import render_template
from flask_mysqldb import MySQL                   # render & return html file

app = Flask(__name__)     


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "issue_tracker"


mysql = MySQL(app)                          # instance of class


@app.route("/")                                     # root URL
def index():
    return render_template("index.html")


@app.route("/test-db")                              # DB connection
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        cursor.close()

        return f"Connected Successfully! Current Database: {result[0]}"

    except Exception as e:
        return f"Database Connection Failed: {e}"


if __name__ == "__main__":                          #directly run
    app.run(debug=True)