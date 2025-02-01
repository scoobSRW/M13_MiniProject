from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


# employee
class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)

    # optional: an additional field can be added if needed
    def __repr__(self):
        return f"<Employee {self.name}>"


# product
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # relationship: one product can be in many orders and production records
    orders = relationship("Order", back_populates="product", cascade="all, delete")
    productions = relationship(
        "Production", back_populates="product", cascade="all, delete"
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# customer
class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    # relationship: one customer can place many orders
    orders = relationship("Order", back_populates="customer", cascade="all, delete")
    account = relationship("CustomerAccount", uselist=False, back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.name}>"


# customer accounts
class CustomerAccount(db.Model):
    __tablename__ = "customer_accounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), unique=True, nullable=False
    )
    customer = relationship("Customer", back_populates="account")


# order
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    # relationships
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}: {self.quantity} of Product {self.product_id}>"


# production
class Production(db.Model):
    __tablename__ = "production"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    date_produced = db.Column(db.Date, nullable=False)
    # relationship: production relates to a specific product
    product = relationship("Product", back_populates="productions")

    def __repr__(self):
        return f"<Production {self.id}: {self.quantity_produced} of Product {self.product_id}>"


# user model
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship(
        "Role", secondary=user_roles, backref=db.backref("users", lazy="dynamic")
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.role_name}>"
