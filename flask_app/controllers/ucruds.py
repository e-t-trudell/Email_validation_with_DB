from flask import Flask, render_template, redirect, request, session
from flask_app.models.ucrud import User
from flask_app import app

@app.route("/users")
def index():
    # from flask_app.models.model_one import User
    # call the get all classmethod to get all users
    users = User.get_all()
    print(users)
    # users=User.getall()
    return render_template("create.html", users=User.get_all())
    

@app.route('/create_user', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/users')
    data = {
        "fname": request.form["first_name"],
        "lname" : request.form["last_name"],
        "email" : request.form["email"]
        }
    # We pass the data dictionary into the save method from the Friend class.
    User.save(data)
    new_user = User.get_last()
    id = new_user.id
    # Redirect after saving to the database.
    return redirect(f'/users/show/{id}')

# show redirects to display which renders read_one for user
@app.route("/users/show/<int:id>")
def show(id):
    data = {'id':id}
    # this variable here lets me use users on the rendered html page rather than running a forloop
    users = User.get_one(data)
    print(users)
    # one_user = data['id']
    return render_template("read_one.html", users = User.get_one(data))

# displays all users
@app.route("/users/displayall")
def displayall():
    users = User.get_all()
    print("Displaying All USERS!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(users)
    return render_template("read_all.html", users=User.get_all())


# this live in an a tag so no psot method needed
@app.route("/users/edit/<int:id>")
def editme(id):
    data = {'id':id}
    users = User.get_one(data)
    print(users)
    return render_template("users_edit.html", users=User.get_one(data))

# new  route method must be post method for update user here + redirect to read_one
@app.route('/users/update_user/<int:id>', methods=["POST"])
def update_user(id):
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "id" : id,
        "fname": request.form["first_name"],
        "lname" : request.form["last_name"],
        "email" : request.form["email"]}
    # We pass the data dictionary into the save method from the Friend class.
    User.save(data)
    # Redirect after saving to the database.
    return redirect(f'/users/show/{id}')

# dont need a post method here if using an a tag for the button
@app.route("/users/destroy/<int:id>")
def destroy(id):
    data = {'id':id}
    User.destroy(data)
    return redirect("/users/displayall")