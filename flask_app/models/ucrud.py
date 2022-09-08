from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    # could enter variable here and set it = to schema name in workbench
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Now we use class methods to query our database
    @staticmethod
    def validate_user( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['first_name']): 
            flash("Do you have a first name?")
            is_valid = False
        if not EMAIL_REGEX.match(user['last_name']): 
            flash("Do you have a last name?")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email!")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # name in parenthesis is the schema name! or variable called jsut after class name.db
        results = connectToMySQL('users_CR').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        # print(users)
        return users

    @classmethod
    def get_one(cls, data):
        # greabs specific id row
        query = 'SELECT * from users WHERE id = %(id)s;'
        results = connectToMySQL('users_CR').query_db(query, data)
        print(results)
        # users = []
        # for user in results:
        #     users.append( cls(user) )
        return cls(results[0])

    @classmethod
    def get_last(cls):
        query = "SELECT * from USERS"
        results = connectToMySQL('users_CR').query_db(query)
        print(results)
        return cls(results[len(results)-1])
        
    # class method to save our user to the database
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(email)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        results = connectToMySQL('users_CR').query_db( query, data )
        return results

    @classmethod
    def destroy(cls, data ):
        # element in %()s is the key from the dictionary in the route
        query = "DELETE FROM users WHERE id=%(id)s;"
        results= connectToMySQL('users_CR').query_db( query, data )
        return results

    @classmethod
    def update(cls, data):
        # updating first name to injection, lastname to injection, email to injection, update on NOW(), where the id is the id referenced
        query = """UPDATE users SET first_name =%(first_name)s, last_name=%(last_name)s, email= %(email)s,
        updated_at = NOW()
        WHERE id = %(ids)"""
        results = connectToMySQL('users_CR').query_db( query, data )
        return results

    