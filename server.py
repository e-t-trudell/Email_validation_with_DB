# STEP THREE
from operator import methodcaller
from flask_app.controllers import ucruds
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)