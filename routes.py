from app import app
from flask import render_template, request, redirect, url_for
from utils import users, groups, messages, tags


@app.route("/")
def index():
    if users.user_id() == 0:
        return redirect("/login")
    else:
        list = groups.get_list()
        username = users.get_user()
        return render_template("index.html", groups=list, username=username[0], type=0)


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


@app.route("/create", methods=["GET", "POST"])
def create_group():
    if users.user_id() == 0:
        return redirect("/login")
    else:
        if request.method == "GET":
            return render_template("create.html")
        if request.method == "POST":
            name = request.form["name"]
            info = request.form["info"]
            tags = request.form["tags"]
            limit = request.form["limit"]
            id = groups.new_group(name, info, tags, limit)
            if id:
                return redirect(url_for("chat", id=id))
            else:
                return render_template("error.html", message="Failed to create a chat")


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
    if users.user_id() == 0:
        return redirect("/login")
    else:
        search_filter = request.args["query"]
        if not search_filter:
            return redirect("/")
        else:
            list = groups.get_filtered_groups(search_filter.lower())
            username = users.get_user()
            return render_template("index.html", groups=list, username=username[0], type=1)


@app.route("/messages/<int:id>", methods=["GET", "POST"])
def chat(id):
    if users.user_id() == 0:
        return redirect("/login")
    else:
        if request.method == "GET":
            list = messages.get_messages(id)
            name = groups.get_name(id)
            member = groups.is_a_member(id)
            return render_template("chat.html", name=name[0], messages=list, id=id, member=member)
        if request.method == "POST":
            content = request.form["content"]
            if messages.send(content, id):
                return redirect(url_for("chat", id=id))
            else:
                return render_template("error.html", message="Failed to send the message")


@app.route("/view/<int:id>")
def view(id):
    if users.user_id() == 0:
        return redirect("/login")
    else:
        group = groups.get_info(id)
        member_count = groups.get_member_count(id)
        members = groups.get_members(id)
        tag_list = tags.get_tags(id)
        return render_template("view.html", group=group, member_count=member_count, members=members, tag_list=tag_list)


@app.route("/leave/<int:id>", methods=["POST"])
def leave(id):
    if users.user_id() == 0:
        return redirect("/login")
    else:
        if groups.leave_a_group(id):
            return redirect("/")
        else:
            return render_template("error", message="Failed to leave the group")


@app.route("/delete")
def delete_user():
    if users.user_id() == 0:
        return redirect("/login")
    else:
        if users.delete():
            return redirect("/")
        else:
            return render_template("error.html", message="Failed to delete the user")


@app.route("/join/<int:id>", methods=["POST"])
def join(id):
    if users.user_id() == 0:
        return redirect("/login")
    else:
        if groups.join_a_group(id):
            return redirect(url_for("chat", id=id))
        else:
            return render_template("error.html", message="Failed to join the group")
