from app import app
from flask import render_template, request, redirect
from SQL import users, groups, messages


@app.route("/")
def index():
    if users.user_id() == 0:
        return redirect("/login")
    else:
        list = groups.get_list()
        return render_template("index.html", groups=list)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Incorrect username or password")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Failed to register")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")


@app.route("/search")
def search():
    search_filter = request.args["query"]
    if not search_filter:
        return redirect("/")
    else:
        list = groups.get_filtered_groups(search_filter)
        return render_template("index.html", groups=list)


@app.route("/messages/<int:id>", methods=["GET", "POST"])
def chat(id):
    if request.method == "GET":
        list = messages.get_messages(id)
        name = groups.get_name(id)
        return render_template("chat.html", name=name[0], messages=list, id=id)
    if request.method == "POST":
        content = request.form['content']
        if messages.send(content, id):
            return redirect("/messages", (id))
        else:
            return render_template("error.html", message="Failed to send the message")
