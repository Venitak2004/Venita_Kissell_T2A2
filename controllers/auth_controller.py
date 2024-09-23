from init import bcrypt, db
from models.user import User, user_schema, UserSchema
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        #body of the auth requesting to GET the information from the database
        body_data = UserSchema().load(request.get_json())
        #create a new user model object, and store hashed password in the model
        user = User(
            name = body_data.get("name"),
            email = body_data.get("email"),
        )
        #now hash the password
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf8")

        #add the new secure encrypted password to the database
        db.session.add(user)
        db.session.commit()    

        #send acknowledgement to user, 201 successful
        return user_schema.dump(user), 201
    #Error codes for invalid entries, cannot be null, and invalid email format
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # returns invalid email must be unique email
            return {"error": "Email address must be unique"}, 400



@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Get the data from the body requesting authorisation for login
    body_data = request.get_json()
    # Search the database to find the user with that matching email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    # If user exists in the database and password is correct, return login
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create JWT token for secure login
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=15))
        # Respond back with the generated token 
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    # Else
    else:
        # Respond back with an error message
        return {"Error": "Invalid email or password, please check and try again"}, 400
    
# /auth/users/user_id
@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    # get the fields from the body of the request from the user table
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # GET the user from the USER database
    # SELECT * FROM user WHERE id= get_jwt_identity() get user identity from the database
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # if the user exists in the database, then:
    if user:
        # update the required fields
        user.name = body_data.get("name") or user.name
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # then commit all entries to the database
        db.session.commit()
        # return to the user 
        return user_schema.dump(user)
    # else return error reply user does not exist in database
    else:
       
        return {"Error": "The User does not exist in the database."}
