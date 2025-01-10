from flask import Blueprint, jsonify, request
from app.models.models import Production, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

production_bp = Blueprint('production', __name__)

# record a production entry (5 requests per minute)
@production_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def record_production():
    data = request.get_json()
    new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'message': 'Production recorded successfully'}), 201

# get all production records (10 requests per minute)
@production_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_production():
    production_records = Production.query.all()
    return jsonify([
        {'id': record.id, 'product_id': record.product_id, 'quantity_produced': record.quantity_produced, 'date_produced': record.date_produced.isoformat()}
        for record in production_records
    ]), 200
