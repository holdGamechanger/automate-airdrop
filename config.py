# config.py
"""
Configuration settings for the Crypto Airdrop Automation project on Solana.
Update these settings with your network details and token parameters.
"""

# Solana RPC URL (e.g., mainnet-beta, testnet, or devnet)
SOLANA_RPC_URL = "https://api.devnet.solana.com"

# SPL Token Mint Address (the token you wish to distribute)
# Replace with your token's mint address.
TOKEN_MINT_ADDRESS = "YourTokenMintAddress"  # e.g., "So11111111111111111111111111111111111111112"

# Wallet private key (a list of integers representing the secret key).
# This should be kept secure and never exposed publicly.
# Example (dummy key – replace with your own):
WALLET_PRIVATE_KEY = [

]

# Sender's Associated Token Account Address for the token.
# This is the token account from which tokens will be sent.
SENDER_TOKEN_ACCOUNT = "SenderAssociatedTokenAccountAddress"

# List of recipient wallet addresses (public keys) for the airdrop.
RECIPIENT_ADDRESSES = [
    "RecipientPublicKey1",
    "RecipientPublicKey2",
    "RecipientPublicKey3",
    # Add more addresses as needed
]

# Amount of tokens to airdrop per address.
# Note: This value should be expressed in the smallest unit (taking token decimals into account).
TOKEN_AMOUNT = 100  # Example: 100 tokens (adjust according to your token's decimals)
