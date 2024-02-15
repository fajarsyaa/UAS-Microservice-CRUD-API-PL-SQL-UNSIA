from flask import jsonify, request
from app import app, db
from app.models import Customer, Merchant, Transaction
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
    key = os.urandom(16)
    ciphertext = base64.b64decode(encrypted_password.encode())
    backend = default_backend()
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    password = unpadder.update(padded_data) + unpadder.finalize()
    return password.decode()


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

