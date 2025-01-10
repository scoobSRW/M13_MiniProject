from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models.models import db
import os


# factory funcs
def create_app(config_class):
    app = Flask(
        __name__,
        static_folder=os.path.join(os.getcwd(), 'static')  # Explicitly set static folder path
    )
    app.config.from_object(config_class)


    # set extensions
    db.init_app(app)
    Migrate(app, db)
    limiter = Limiter(get_remote_address, app=app)

    # validate blueprints
    from app.blueprints.employees.routes import employees_bp
    from app.blueprints.products.routes import products_bp
    from app.blueprints.orders.routes import orders_bp
    from app.blueprints.customers.routes import customers_bp
    from app.blueprints.production.routes import production_bp
    from app.blueprints.users.routes import users_bp
    from app.blueprints.swagger import swagger_blueprint

    app.register_blueprint(employees_bp, url_prefix='/api/employees')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(production_bp, url_prefix='/api/production')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(swagger_blueprint, url_prefix='/api/docs')

    return app