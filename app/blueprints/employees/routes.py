from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.models.models import Employee, db

limiter = Limiter(get_remote_address)

employees_bp = Blueprint("employees", __name__)


# Create an employee (5 requests per minute)
@employees_bp.route("", methods=["POST"])
@limiter.limit("5 per minute")
def create_employee():
    data = request.get_json()
    new_employee = Employee(name=data["name"], position=data["position"])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee created successfully"}), 201


# Get all employees (10 requests per minute)
@employees_bp.route("", methods=["GET"])
@limiter.limit("10 per minute")
def get_employees():
    employees = Employee.query.all()
    return (
        jsonify(
            [
                {"id": emp.id, "name": emp.name, "position": emp.position}
                for emp in employees
            ]
        ),
        200,
    )


# Update an employee (5 requests per minute)
@employees_bp.route("/<int:employee_id>", methods=["PUT"])
@limiter.limit("5 per minute")
def update_employee(employee_id):
    data = request.get_json()
    employee = Employee.query.get_or_404(employee_id)
    employee.name = data.get("name", employee.name)
    employee.position = data.get("position", employee.position)
    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200


# Delete an employee (5 requests per minute)
@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
@limiter.limit("5 per minute")
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200
