from flask import Flask, request, jsonify
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

# Chave de 16 bytes (128 bits)
KEY = b'chavesecreta123'

# Função para adicionar padding à mensagem
def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

# Criptografar a mensagem
def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(message).encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Descriptografar a mensagem
def decrypt_message(encrypted_message):
    cipher = AES.new(KEY, AES.MODE_ECB)
    decoded_encrypted = base64.b64decode(encrypted_message)
    decrypted = cipher.decrypt(decoded_encrypted).decode('utf-8').rstrip()
    return decrypted

# Endpoint para enviar uma mensagem
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    encrypted_message = encrypt_message(message)
    # Aqui você pode salvar a mensagem criptografada em um banco de dados
    return jsonify({'encrypted_message': encrypted_message})

# Endpoint para receber e descriptografar a mensagem
@app.route('/receive_message', methods=['POST'])
def receive_message():
    data = request.get_json()
    encrypted_message = data.get('encrypted_message')
    decrypted_message = decrypt_message(encrypted_message)
    return jsonify({'decrypted_message': decrypted_message})

if __name__ == '__main__':
    app.run(debug=True)
