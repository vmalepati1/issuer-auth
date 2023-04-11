from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Signer
from stellar_sdk import Asset
import requests

# Initialize server and keypairs for accounts
server = Server("https://horizon-testnet.stellar.org")
root_keypair = Keypair.from_secret("SDWMLW4MU4Z355EGDCVUZVHVMVLZ556FA62KJNFPXLTY2N6QY7OT6ZYZ")
child1_keypair = Keypair.from_secret("SBUYEACBGMCFX6CLUCIOLH5DORVGAZX5OQDH5FGLZLH5G2UIGBZAUHJB")
child2_keypair = Keypair.from_secret("SDRDMLYVVADPE2ASP7QIXNZAOWWXBL5URTIPHVYP5PUPJVAYXTMB6IY4")

# Add signers to the root account
root_account = server.load_account(root_keypair.public_key)

# Create random dest account
pair = Keypair.random()
print(f"Dest Secret: {pair.secret}")
# Secret: SADWIQXRSDP4GRF7REQ2KNNZD64PATUAIYANLYGGO6YQ6IWKQP3KT57C
print(f"Dest Public Key: {pair.public_key}")
# Public Key: GD6YBMHQKWXAFV34FSRQ6SZ2IGJ3JYY5B5A2Y574OU4ZIDD3PDV2DBD2

dest = pair.public_key

response = requests.get(f"https://friendbot.stellar.org?addr={dest}")

# Build and sign the transaction
transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(asset=Asset.native(), destination=dest, amount="10")
    .set_timeout(30)
    .build()
)

# Sign the transaction with the root account and both child accounts
# transaction.sign(root_keypair)
transaction.sign(child1_keypair)
transaction.sign(child2_keypair)

# Submit the transaction to the network
response = server.submit_transaction(transaction)
print(f"Transaction hash: {response['hash']}")
