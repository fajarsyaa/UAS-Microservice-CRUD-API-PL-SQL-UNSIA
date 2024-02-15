from flask import jsonify, request, Flask, session
from app import app, db
from sqlalchemy import text
from app.middleware.loginMiddleware import check_login_customer


# add payment
@app.route('/payment', methods=['POST'])
def create_payment():
    if check_login_customer(session.get('customer'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 
    
    data = request.get_json()
    customer_id = data.get('customer_id')
    merchant_id = data.get('merchant_id')
    amount = data.get('amount')

    if not (customer_id and merchant_id and amount):
        return jsonify({'error': 'Incomplete data provided'}), 400

    try:
        query = text("INSERT INTO trx_payment (customer_id, merchant_id, amount) VALUES (:customer_id, :merchant_id, :amount)")
        db.session.execute(query, {"customer_id": customer_id, "merchant_id": merchant_id, "amount": amount})
        db.session.commit()
        return jsonify({'message': 'Payment created successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create payment', 'details': str(e)}), 500


# Get  payment
@app.route('/payment/<int:id>', methods=['GET'])
def get_payments_id(id):
    if check_login_customer(session.get('customer'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 
    
    try:
        query = text("SELECT tp.id, mm.username, mc.username, tp.amount FROM trx_payment tp JOIN ms_customer mc ON tp.customer_id = mc.id JOIN ms_merchant mm ON tp.merchant_id = mm.id WHERE tp.id = :id;")
        result = db.session.execute(query,{'id': id})
        result_array = [row for row in result]

        result_dicts = [{'id': row[0],'merchat': row[1], 'customer': row[2], 'amount' : row[3]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve payments', 'details': str(e)}), 500

# Get all payment
@app.route('/payment', methods=['GET'])
def get_payments():
    try:
        query = text("SELECT tp.id, mm.username, mc.username, tp.amount FROM trx_payment tp JOIN ms_customer mc ON tp.customer_id = mc.id JOIN ms_merchant mm ON tp.merchant_id = mm.id;")
        result = db.session.execute(query)
        result_array = [row for row in result]

        result_dicts = [{'id': row[0],'merchat': row[1], 'customer': row[2], 'amount' : row[3]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve payments', 'details': str(e)}), 500

