from flask import jsonify, request, Flask, session
from hashlib import sha256
from base64 import b64encode, b64decode
from app import app, db
from app.models import  Merchant
from app.middleware.loginMiddleware import check_login_merchant, check_login
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
    if check_login_merchant(session.get('user'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 

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
    if check_login_merchant(session.get('user'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    no_rek = data.get('no_rek')

    if not (username and email and password and no_rek):
        return jsonify({'error': 'Incomplete data provided'}), 400

    try:        
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
    if check_login_merchant(session.get('user'),session.get('level')) : 
       return jsonify({'error': 'Access Forbidden'}), 403 

    try:
        query = text("DELETE FROM ms_merchant WHERE id=:id")
        db.session.execute(query,  {'id': id})
        db.session.commit()
        return jsonify({'message': 'Merchant deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete merchant', 'details': str(e)}), 500


# login merchant
@app.route('/login/merchant', methods=['POST'])
def login_merchant():
    if check_login(session.get('user')):
        return jsonify({'error': 'Login Already'}), 403

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({'error': 'Incomplete data provided'}), 400    

    try:
        merchant = Merchant.query.filter_by(email=email).first()
        if merchant:    
            if password == decrypt_password(merchant.password):  
                session['user'] = merchant.username                         
                session['level'] = "merchant"
                return jsonify({'message': 'Login successful'}), 200
            else:                
                return jsonify({'error': 'Incorrect password'}), 401
        else:            
            return jsonify({'error': 'Customer not registered'}), 404
    except SQLAlchemyError as e:        
        return jsonify({'error': 'Database error'}), 500