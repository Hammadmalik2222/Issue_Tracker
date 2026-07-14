from flask import Flask                             # import class
from flask import render_template
from flask_mysqldb import MySQL 
from flask import request                  # render & return html file

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

@app.route("/create-issue", methods=["GET", "POST"])
def add_issue():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        severity = request.form["severity"]
        reported_by = request.form["reported_by"]
        assigned_to = request.form["assigned_to"]
        firefox_version = request.form["firefox_version"]
        is_security_issue = request.form["is_security_issue"]


        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO issues
            (
            title,
            description,
            severity,
            reported_by,
            assigned_to,
            firefox_version,
            is_security_issue
            )

            VALUES (%s,%s,%s,%s,%s,%s,%s)

        """,
        (
        title,
        description,
        severity,
        reported_by,
        assigned_to,
        firefox_version,
        is_security_issue
        ))


        mysql.connection.commit()

        cursor.close()

        return "Issue Added Successfully"


    return render_template("create_issue.html")


@app.route("/read-issue")
def view_issues():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM issues")

    issues = cursor.fetchall()

    cursor.close()

    return render_template("read_issue.html", issues=issues)

if __name__ == "__main__":                          #directly run
    app.run(debug=True)