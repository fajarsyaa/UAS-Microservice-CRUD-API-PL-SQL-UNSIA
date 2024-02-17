from flask import jsonify, request, Flask, session
from hashlib import sha256
from base64 import b64encode, b64decode
from app import app, db
from app.models import Customer
from app.middleware.loginMiddleware import check_login_customer, check_login
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

key = sha256(os.urandom(32)).digest()

def encrypt_password(plaintext):
    iv = os.urandom(16)    
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return b64encode(iv + ciphertext).decode()

def decrypt_password(ciphertext):    
    ciphertext = b64decode(ciphertext.encode())    
    iv = ciphertext[:16]    
    ciphertext = ciphertext[16:]    
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return plaintext


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
    

    try:
        encrypted_password = encrypt_password(password)       
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
    
    if check_login_customer(session.get('user'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 

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
    if check_login_customer(session.get('user'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 
    
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
    if check_login_customer(session.get('user'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 

    try:
        query = text("DELETE FROM ms_customer WHERE id=:id")
        db.session.execute(query,  {'id': id})
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete customer', 'details': str(e)}), 500

# login customer
@app.route('/login/customer', methods=['POST'])
def login_customer():
    if check_login(session.get('user')):
        return jsonify({'error': 'Login Already'}), 403

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({'error': 'Incomplete data provided'}), 400    

    try:
        customer = Customer.query.filter_by(email=email).first()
        if customer:    
            if password == decrypt_password(customer.password):  
                session['user'] = customer.username                         
                session['level'] = "customer"
                return jsonify({'message': 'Login successful'}), 200
            else:                
                return jsonify({'error': 'Incorrect password'}), 401
        else:            
            return jsonify({'error': 'Customer not registered'}), 404
    except SQLAlchemyError as e:        
        return jsonify({'error': 'Database error'}), 500
    
# logout
@app.route('/logout', methods=['POST'])
def logout():
    if session.get('user') and session.get('level'):
        session.pop('user', None)
        session.pop('level', None)
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'Not logged in'}), 401    