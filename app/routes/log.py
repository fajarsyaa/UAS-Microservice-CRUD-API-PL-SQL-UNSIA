from flask import jsonify, request
from app import app, db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


# Get all payment log
@app.route('/log/payment', methods=['GET'])
def get_payments_log():
    try:
        query = text("SELECT action, customer_id, merchant_id, amount, changed_at FROM trx_payment_log;")
        result = db.session.execute(query)
        result_array = [row for row in result]

        result_dicts = [{'action': row[0],'merchat': row[1], 'customer': row[2], 'amount' : row[3],'changed_at' : row[4]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve payments logs', 'details': str(e)}), 500

# Get all merchant log
@app.route('/log/merchant', methods=['GET'])
def get_merchant_log():
    try:
        query = text("SELECT action, username, email, password, no_rek,changed_at FROM ms_merchant_log;")
        result = db.session.execute(query)
        result_array = [row for row in result]

        result_dicts = [{'action': row[0],'username': row[1], 'email': row[2], 'password' : row[3],'no_rek' : row[4],'changed_at' : row[5]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve merchant logs', 'details': str(e)}), 500

# Get all customer log
@app.route('/log/customer', methods=['GET'])
def get_customer_log():
    try:
        query = text("SELECT action, username, email, password, no_rek,changed_at FROM ms_customer_log;")
        result = db.session.execute(query)
        result_array = [row for row in result]

        result_dicts = [{'action': row[0],'username': row[1], 'email': row[2], 'password' : row[3],'no_rek' : row[4],'changed_at' : row[5]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve customer logs', 'details': str(e)}), 500
