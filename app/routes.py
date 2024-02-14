from flask import jsonify, request
from app import app, db
from app.models import Customer, Merchant
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

# Fungsi untuk mengenkripsi password menggunakan AES
def encrypt_password(password):
    key = os.urandom(16)
    backend = default_backend()
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode()

# Fungsi untuk mendekripsi password menggunakan AES
def decrypt_password(encrypted_password):
    ciphertext = base64.b64decode(encrypted_password.encode())
    backend = default_backend()
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    password = unpadder.update(padded_data) + unpadder.finalize()
    return password.decode()

# add customer
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    no_rek = data.get('no_rek')

    if not (username and email and password and no_rek):
        return jsonify({'error': 'Incomplete data provided'}), 400
    
    encrypted_password = encrypt_password(password)

    try:
        query = text("INSERT INTO ms_customer (username, email, password, no_rek) VALUES (:username, :email, :password, :no_rek)")
        db.session.execute(query, {"username": username, "email": email, "password": encrypted_password, "no_rek": no_rek})
        db.session.commit()
        return jsonify({'message': 'Customer created successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create customer', 'details': str(e)}), 500


# Get all customer
@app.route('/customer', methods=['GET'])
def get_customers():
    try:
        query = text("SELECT id, username, email, no_rek FROM ms_customer")
        result = db.session.execute(query)
        result_array = [row for row in result]

        result_dicts = [{'id': row[0],'username': row[1], 'email': row[2], 'no_rek' : row[3]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve customers', 'details': str(e)}), 500


# Update customer
@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    no_rek = data.get('no_rek')

    if not (username and email and password and no_rek):
        return jsonify({'error': 'Incomplete data provided'}), 400

    try:
        # Enkripsi password baru
        encrypted_password = encrypt_password(password)
        query = text("UPDATE ms_customer SET username=:username, email=:email, password=:password, no_rek=:no_rek WHERE id=:id")
        db.session.execute(query, {'id': id, 'username': username, 'email': email, 'password': encrypted_password, 'no_rek': no_rek})
        db.session.commit()

        return jsonify({'message': 'Customer updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update customer', 'details': str(e)}), 500

# Delete customer
@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        query = text("DELETE FROM ms_customer WHERE id=:id")
        db.session.execute(query,  {'id': id})
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete customer', 'details': str(e)}), 500


# add merchant
@app.route('/merchant', methods=['POST'])
def create_merchant():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    no_rek = data.get('no_rek')

    if not (username and email and password and no_rek):
        return jsonify({'error': 'Incomplete data provided'}), 400
    
    encrypted_password = encrypt_password(password)

    try:
        query = text("INSERT INTO ms_merchant (username, email, password, no_rek) VALUES (:username, :email, :password, :no_rek)")
        db.session.execute(query, {"username": username, "email": email, "password": encrypted_password, "no_rek": no_rek})
        db.session.commit()
        return jsonify({'message': 'merchant created successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create merchant', 'details': str(e)}), 500


# Get all merchant
@app.route('/merchant', methods=['GET'])
def get_merchants():
    try:
        query = text("SELECT id, username, email, no_rek FROM ms_merchant")
        result = db.session.execute(query)
        result_array = [row for row in result]

        result_dicts = [{'id': row[0],'username': row[1], 'email': row[2], 'no_rek' : row[3]} for row in result_array]

        if not result_dicts:            
            return jsonify([]), 200 
        
        return jsonify(result_dicts), 200
    except Exception as e:        
        return jsonify({'error': 'Failed to retrieve merchants', 'details': str(e)}), 500


# Update merchant
@app.route('/merchant/<int:id>', methods=['PUT'])
def update_merchant(id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    no_rek = data.get('no_rek')

    if not (username and email and password and no_rek):
        return jsonify({'error': 'Incomplete data provided'}), 400

    try:
        # Enkripsi password baru
        encrypted_password = encrypt_password(password)
        query = text("UPDATE ms_merchant SET username=:username, email=:email, password=:password, no_rek=:no_rek WHERE id=:id")
        db.session.execute(query, {'id': id, 'username': username, 'email': email, 'password': encrypted_password, 'no_rek': no_rek})
        db.session.commit()

        return jsonify({'message': 'merchant updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update merchant', 'details': str(e)}), 500

# Delete merchant
@app.route('/merchant/<int:id>', methods=['DELETE'])
def delete_merchant(id):
    try:
        query = text("DELETE FROM ms_merchant WHERE id=:id")
        db.session.execute(query,  {'id': id})
        db.session.commit()
        return jsonify({'message': 'Merchant deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete merchant', 'details': str(e)}), 500


# add payment
@app.route('/payment', methods=['POST'])
def create_payment():
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


# Get all payment
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
