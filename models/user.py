from init import db, ma

#Create the user table inside User Model to create the columns
class User(db.Model):
    __tablename__ = "users"
    #install the user table attributes
    #define the primary key for data serialisation
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    display_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    #create the admin user login is True
    is_admin = db.Column(db.Boolean, default=False)

#create the user schema class to action table seeding
class UserSchema(ma.Schema):
   class Meta:
       fields = ("id", "name", "email", "password", "is_admin")

#activate the user schema/schemas for singular and multiple instances.
user_schema = UserSchema()
user_schemas = UserSchema(many=True, exclude=["password"])