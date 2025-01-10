from wsgi import app
from datetime import date
from app.models.models import db, User, Role, Employee, Product, Customer, Order, Production
from werkzeug.security import generate_password_hash


def seed_database():
    try:
        with app.app_context():
            # Drop all tables and recreate them
            db.drop_all()
            db.create_all()

            # Seed Roles
            roles = [
                {'role_name': 'admin'},
                {'role_name': 'employee'},
                {'role_name': 'user'}
            ]

            for role_data in roles:
                if not Role.query.filter_by(role_name=role_data['role_name']).first():
                    role = Role(role_name=role_data['role_name'])
                    db.session.add(role)

            # Seed Users with Role Assignment
            users = [
                {'username': 'user1', 'password': 'adminpassword', 'roles': ['admin']},
                {'username': 'user2', 'password': 'emppassword', 'roles': ['employee']},
                {'username': 'user3', 'password': 'userpassword', 'roles': ['user']}
            ]

            for user_data in users:
                if not User.query.filter_by(username=user_data['username']).first():
                    user = User(
                        username=user_data['username'],
                        password=generate_password_hash(user_data['password'])
                    )
                    for role_name in user_data['roles']:
                        role = Role.query.filter_by(role_name=role_name).first()
                        if role:
                            user.roles.append(role)
                    db.session.add(user)

            # Seed Employees
            employees = [
                {'name': 'John Doe', 'position': 'Manager'},
                {'name': 'Jane Smith', 'position': 'Salesperson'}
            ]

            for emp_data in employees:
                if not Employee.query.filter_by(name=emp_data['name']).first():
                    employee = Employee(name=emp_data['name'], position=emp_data['position'])
                    db.session.add(employee)

            # Seed Products
            products = [
                {'name': 'Widget', 'price': 9.99},
                {'name': 'Gadget', 'price': 19.99}
            ]

            for prod_data in products:
                if not Product.query.filter_by(name=prod_data['name']).first():
                    product = Product(name=prod_data['name'], price=prod_data['price'])
                    db.session.add(product)

            # Seed Customers
            customers = [
                {'name': 'Alice Johnson', 'email': 'alice@example.com', 'phone': '123-456-7890'},
                {'name': 'Bob Brown', 'email': 'bob@example.com', 'phone': '987-654-3210'}
            ]

            for cust_data in customers:
                if not Customer.query.filter_by(email=cust_data['email']).first():
                    customer = Customer(
                        name=cust_data['name'], email=cust_data['email'], phone=cust_data['phone']
                    )
                    db.session.add(customer)

            # Seed Orders
            customer1 = Customer.query.filter_by(email='alice@example.com').first()
            customer2 = Customer.query.filter_by(email='bob@example.com').first()
            product1 = Product.query.filter_by(name='Widget').first()
            product2 = Product.query.filter_by(name='Gadget').first()

            orders = [
                {'customer_id': customer1.id, 'product_id': product1.id, 'quantity': 2, 'total_price': 19.98},
                {'customer_id': customer2.id, 'product_id': product2.id, 'quantity': 1, 'total_price': 19.99}
            ]

            for order_data in orders:
                if not Order.query.filter_by(customer_id=order_data['customer_id'], product_id=order_data['product_id']).first():
                    order = Order(
                        customer_id=order_data['customer_id'],
                        product_id=order_data['product_id'],
                        quantity=order_data['quantity'],
                        total_price=order_data['total_price']
                    )
                    db.session.add(order)

            # Seed Production Records
            productions = [
                {'product_name': 'Widget', 'quantity_produced': 100, 'date_produced': date(2023, 12, 25)},
                {'product_name': 'Gadget', 'quantity_produced': 200, 'date_produced': date(2023, 12, 26)}
            ]

            for prod_rec_data in productions:
                product = Product.query.filter_by(name=prod_rec_data['product_name']).first()
                if product and not Production.query.filter_by(product_id=product.id, date_produced=prod_rec_data['date_produced']).first():
                    production = Production(
                        product_id=product.id,
                        quantity_produced=prod_rec_data['quantity_produced'],
                        date_produced=prod_rec_data['date_produced']
                    )
                    db.session.add(production)

            # Commit changes
            db.session.commit()
            print("Database has been seeded with initial data")

    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")


if __name__ == '__main__':
    seed_database()
