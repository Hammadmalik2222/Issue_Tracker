from flask import Flask                             # import class
from flask import render_template
from flask_mysqldb import MySQL 
from flask import request 
from flask import redirect, flash
                # render & return html file


app = Flask(__name__)    
app.secret_key = "firefox_issue_tracker" 


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "issue_tracker"


mysql = MySQL(app)                          # instance of class


@app.route("/")
def home():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM issues")

    total_issues = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "index.html",
        total_issues=total_issues
    )

@app.route("/templates/<path:filename>")
def template(filename):
    return send_from_directory("templates", filename)




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

        flash("Issue added successfully!", "success")

        return redirect("/read-issue")


    return render_template("create_issue.html")


@app.route("/read-issue")
def view_issues():

    cursor = mysql.connection.cursor()

    severity = request.args.get("severity")
    status = request.args.get("status")

    query = "SELECT * FROM issues WHERE 1=1"

    values = []

    if severity:

        query += " AND severity=%s"

        values.append(severity)


    if status:

        query += " AND status=%s"

        values.append(status)


    cursor.execute(query, values)

    issues = cursor.fetchall()

    cursor.close()

    return render_template(
        "read_issue.html",
        issues=issues
    )

@app.route("/update-issue/<int:id>", methods=["GET","POST"])
def update_issue(id):

    cursor = mysql.connection.cursor()


    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        severity = request.form["severity"]
        status = request.form["status"]
        assigned_to = request.form["assigned_to"]
        firefox_version = request.form["firefox_version"]


        cursor.execute("""
        UPDATE issues 
        SET title=%s,
        description=%s,
        severity=%s,
        status=%s,
        assigned_to=%s,
        firefox_version=%s
        WHERE issue_id=%s

        """,
       (
        title,
        description,
        severity,
        status,
        assigned_to,
        firefox_version,
        id
))


        mysql.connection.commit()

        cursor.close()

        flash("Issue updated successfully!", "success")

        return redirect("/read-issue")


    cursor.execute(
        "SELECT * FROM issues WHERE issue_id=%s",
        (id,)
    )

    issue = cursor.fetchone()

    cursor.close()


    return render_template(
        "update_issue.html",
        issue=issue
    )


@app.route("/delete-issue/<int:id>")
def delete_issue(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM issues WHERE issue_id=%s",
        (id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Issue deleted successfully!", "success")

    return redirect("/read-issue")

if __name__ == "__main__":                          #directly run
    app.run(debug=True)