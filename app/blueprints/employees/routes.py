from flask import Blueprint, jsonify, request
from app.models.models import Employee, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

employees_bp = Blueprint('employees', __name__)

# create an employee (5 requests per minute)
@employees_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully'}), 201

# get all employees (10 requests per minute)
@employees_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]), 200
