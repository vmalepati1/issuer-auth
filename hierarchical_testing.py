from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Signer
import requests

# Create a server object for the Stellar network
server = Server("https://horizon-testnet.stellar.org")

# Create the root account
root_keypair = Keypair.random()
print(f"Root Account: {root_keypair.public_key} {root_keypair.secret}")
response = requests.get(f"https://friendbot.stellar.org?addr={root_keypair.public_key}")
print(response.text)

# Create the first child account with low authority
child1_keypair = Keypair.random()
print(f"Child1 Account: {child1_keypair.public_key} {child1_keypair.secret}")
response = requests.get(f"https://friendbot.stellar.org?addr={child1_keypair.public_key}")
print(response.text)

# Create the second child account with high authority
child2_keypair = Keypair.random()
print(f"Child2 Account: {child2_keypair.public_key} {child2_keypair.secret}")
response = requests.get(f"https://friendbot.stellar.org?addr={child2_keypair.public_key}")
print(response.text)

# Build the transaction to add the first child account as a signer for the root account
root_account = server.load_account(account_id=root_keypair.public_key)
transaction = TransactionBuilder(
    source_account=root_account,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=100,
).append_set_options_op(
    master_weight=0,
    low_threshold=1,
    med_threshold=2,
    high_threshold=2,
    signer=Signer.ed25519_public_key(child1_keypair.public_key, weight=1),
).append_set_options_op(
    signer=Signer.ed25519_public_key(child2_keypair.public_key, weight=2),
).build()

# Sign and submit the transaction
transaction.sign(root_keypair)
response = server.submit_transaction(transaction)
print(response)
