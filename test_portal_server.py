from stellar_sdk import Server, Keypair, Signer
from flask import Flask, request, session
from base64 import b64decode
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

stellar_server = Server("https://horizon-testnet.stellar.org")

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_public_key = request.json['public_key']
    challenge = Keypair.random().secret

    send_challenge_to_app(challenge, user_public_key)

    session['challenge'] = challenge
    session['user_public_key'] = user_public_key

    return 'Challenge sent to user', 200

@app.route('/verify', methods=['POST'])
def verify():
    response = request.json['response']
    user_public_key = session['user_public_key']
    challenge = session['challenge']

    # Fetch the account from the Stellar network using the user's public key
    account = stellar_server.accounts().account_id(user_public_key).call()

    # Decode the signature from the app
    signature = b64decode(response)

    # Verify the signature
    if account.verify_challenge(challenge.encode('utf-8'), signature, signer=Signer.ed25519_public_key(user_public_key)):
        # Authentication successful, generate JWT token for user
        token = generate_jwt_token(user_public_key)

        return {'token': token}
    else:
        return 'Authentication failed'

# Function to generate JWT token for user
def generate_jwt_token(user_public_key):
    return 'Success'

# Function to send challenge to user's app
def send_challenge_to_app(challenge, user_public_key):
    endpoint_url = 'http://127.0.0.1:205/authenticate'

    payload = {
        'challenge': challenge,
    }

    url = endpoint_url + '/' + user_public_key

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception('Failed to send challenge to app')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)
    
