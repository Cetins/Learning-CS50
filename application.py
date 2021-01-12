import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from code import get_random_alphanumeric_string

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")

@app.route("/")
@login_required
def index():
    """Show home page for user"""
    rows = db.execute("SELECT code, type, amount, date FROM codes WHERE owner_id = ?", session["user_id"])
    return render_template("index.html", rows=rows)


@app.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
    """Generate Random Unique Code"""

    if request.method == "GET":
        return render_template("generate.html")
    else:
        if not request.form.get("length"):
            return apology("must provide number", 403)

        elif not request.form.get("amount"):
            return apology("must provide amount", 403)

        code_amount = int(request.form.get("amount"))

        if code_amount < 1:
            return apology("minumum amount is 1", 403)

        length = int(request.form.get("length"))
        code_type = request.form.get("type")
        code_amount = request.form.get("amount")
        code = get_random_alphanumeric_string(length)
        owner_id = session["user_id"]
        process = "generated and added to your database"

        db.execute("INSERT INTO codes (owner_id, code, type, amount) VALUES (?, ?, ?, ?)", owner_id, code, code_type, code_amount)

        return render_template("success.html", code=code, process=process)



@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    """Check Code in Database"""

    if request.method == "GET":
        return render_template("check.html")
    else:
        code = request.form.get("code")

        if not request.form.get("code"):
            return apology("must provide code", 403)

        rows = db.execute("SELECT * from codes WHERE code = ? and owner_id = ?", code, session["user_id"])

        if len(rows) == 1:
            process = "found"
            return render_template("checked.html", rows=rows)
        else:
            return apology("sorry code is not valid", 403)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/validate", methods=["GET", "POST"])
@login_required
def validate():
    """Validate your code"""
    if request.method == "GET":
        return render_template("validate.html")
    else:
        code = request.form.get("code")
        owner_id = session["user_id"]

        if not request.form.get("code"):
            return apology("must provide code", 403)

        code_id_list = db.execute("SELECT id from codes WHERE code = ? and owner_id = ?", code, session["user_id"])

        if len(code_id_list) == 1:
            code_id = code_id_list[0]["id"]

            db.execute("DELETE FROM codes WHERE id = ?", code_id)

            check_code = db.execute("SELECT * from codes WHERE code = ? and owner_id = ?", code, owner_id)

            if len(check_code) == 0:
                process = "validated and deleted from database"
                return render_template("success.html", code=code, process=process)
            else:
                return apology("sorry something went wrong, please check your code and try again", 403)
        else:
            return apology("sorry we couldn't find your code", 403)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""


    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        elif not request.form.get("password2"):
            return apology("must re-type password", 403)

        # Check the password match
        if request.form.get("password") != request.form.get("password2"):
            return apology("your passwords didn't match")

        # Query database for existing usernames
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username not exists
        if len(rows) == 1:
            return apology("username exists, please select another")

        # Otherwise insert the user to the users TABLE
        else:
            hashed_pass = generate_password_hash((request.form.get("password")), method='pbkdf2:sha256', salt_length=len(request.form.get("password")))
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                        username=request.form.get("username"), hash=hashed_pass)

        # Return apology if cannot register
        # Query database for username to check
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 1:
            return apology("Sorry something went wrong, please try again")

        # If register succesful
        else:
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)