from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf

VALID_CATEGORY = ("Beauty", "Technology", "Toys", "Furniture", "Sport", "Household Goods", "Electrical", "Other")

#create a model of the product table and define the columns
class Product(db.Model):
    #define the name of the product table
    __tablename__ = "products"
    #define the primary key
    id = db.Column(db.Integer, primary_key=True)
    #define other table attribute columns
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    category = db.column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", nullable=False))

    user = db.relationship("User", back_populates="products")
    reviews = db.relationship("Review", back_populates="product", caascade="all, delete")

#creating the product schema
class ProductSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["product"]))
    category = fields.String(validate=OneOf(VALID_CATEGORY))
    
    
    @validates("status")
    def validate_status(self, value):
        # if trying to see the category exists
        if value == VALID_CATEGORY[1]:
            # check whether an existing Category exists or not
            # SELECT COUNT(*) FROM table_name WHERE status="Technology"
            stmt = db.select(db.func.count()).select_from(Product).filter_by(status=VALID_CATEGORY[1])
            count = db.session.scalar(stmt)
            # if it exists
            if count > 0:
                # send error message
                return ("No category review exists")
                          
    
    class Meta:
        #Fields
        fields = ("id", "name", "description", "category")

#to handle a single product at a time
product_schema = ProductSchema()
#to handle multiple products
product_schemas = ProductSchema(many=True)