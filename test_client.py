from stellar_sdk import Server, Keypair
from flask import Flask, request
import binascii

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xdEEET'

# Initialize Stellar server and keypair
stellar_server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret("SAM2ICVD5WGDQANIPPX6KTJP6BEFKUQSP6XDSTHIMQZ4BVWPQCC2KTJ6")

# Route to handle receiving authentication requests
@app.route('/authenticate/<public_key>', methods=['POST'])
def receive_authentication_request(public_key=''):
    # Get challenge from request
    challenge = request.json['challenge']

    # Sign challenge with user's private key
    signature = keypair.sign(challenge.encode())
    signature_hex = binascii.hexlify(signature).decode() 

    # Send signature back to web dashboard
    send_response_to_dashboard(signature_hex)

##    print(signature)
##    print(signature_hex)

    return 'Challenge signed', 200

# Function to send signature to web dashboard
def send_response_to_dashboard(signature):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=205, debug=True)
