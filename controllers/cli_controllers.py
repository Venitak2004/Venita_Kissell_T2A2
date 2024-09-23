from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.product import Product
from models.review import Review

db_commands = Blueprint("db", __name__)

#create the database tables 
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

#seed the database tables with input values
@db_commands.cli.command("seed")
def seed_tables():
    # Create a list of User instances to populate the user tables
    users = [
        User(
            email = "admin@gmail.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin = True
        ), 
        User(
            name = "Mary Jones",
            email = "maryja@gmail.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8")
        )
    ]
#add all entries to the database
    db.session.add_all(users)

#create a list of entries to populate the product tables
    products = [
        Product(
            name = "Revlon Foundation",
            description = "Revlon ColourStay Foundation",
            category = "Beauty",
            user = users[1]
        ), 
        Product(
            name = "Giant Bike",
            description = "Giant 24inch Mountain bike large wheel",
            category = "Sport",
            user = users[0]            
        ), 
        Product(
            name = "Barbie",
            description = "Barbie Mermaidia",
            category = "Toys",
            user = users[1]
        )]
#seed all products to the products tables
    db.session.add_all(products)

    reviews = [
        Review(
            date = date.today(),
            user = users[0],
            product = products[0],
            rating = "5",
            comment = "Loved this product, it lasts on my skin for 24 hours, without separating"
        ),
        Review(
            date = date.today(),
            user = users[1],
            product = products[0],
            rating = "4",
            comment = "Great pushbike, quality made, great value for the price."
        ),
        Review(
            date = date.today(),
            user = users[0],
            product = products[2],
            rating = "2",
            comment = "The barbie is a bit plasticy, and not very well constructed."
        )
    ]

    db.session.add_all(reviews)
    
    db.session.commit()

    print("Tables seeded!")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")