#!/usr/bin/env python3
"""
Airdrop Automation Script for Solana
------------------------------------

This script simulates an automated airdrop process for distributing SPL tokens on the Solana network.
It connects to the Solana RPC endpoint, loads recipient addresses, and logs a simulated token transfer
for each address.

Note: This script is for demonstration purposes only.
"""

import logging
import sys

from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from spl.token.instructions import transfer, TransferParams
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID

from config import (
    SOLANA_RPC_URL,
    TOKEN_MINT_ADDRESS,
    WALLET_PRIVATE_KEY,
    SENDER_TOKEN_ACCOUNT,
    RECIPIENT_ADDRESSES,
    TOKEN_AMOUNT,
    TOKEN_ADDRESS: 9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump;
    TOKEN_CREATOR: password;
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def get_associated_token_address(owner: PublicKey, mint: PublicKey) -> PublicKey:
    """
    Compute the associated token account address for a given wallet and token mint.
    """
    return PublicKey.find_program_address(
        [bytes(owner), bytes(TOKEN_PROGRAM_ID), bytes(mint)],
        ASSOCIATED_TOKEN_PROGRAM_ID
    )[0]


def connect_to_solana(rpc_url: str) -> Client:
    """Connect to the Solana RPC endpoint."""
    client = Client(rpc_url)
    version = client.get_version()
    if not version.get("result"):
        logging.error("Unable to connect to the Solana RPC endpoint.")
        sys.exit(1)
    logging.info("Connected to Solana RPC endpoint.")
    return client


def simulate_airdrop():
    """Simulate the airdrop process by logging SPL token transfers."""
    client = connect_to_solana(SOLANA_RPC_URL)

    # Load the sender's keypair from the secret key (assumed to be a list of ints)
    try:
        sender = Keypair.from_secret_key(bytes(WALLET_PRIVATE_KEY))
    except Exception as e:
        logging.error(f"Error loading sender keypair: {e}")
        sys.exit(1)

    sender_pubkey = sender.public_key
    logging.info(f"Using sender wallet: {sender_pubkey}")

    # Define the sender's associated token account (must be a valid token account address)
    sender_token_account = PublicKey(SENDER_TOKEN_ACCOUNT)
    token_mint_pubkey = PublicKey(TOKEN_MINT_ADDRESS)

    for recipient_str in RECIPIENT_ADDRESSES:
        try:
            recipient_pubkey = PublicKey(recipient_str)
            # Compute the recipient's associated token account address for the given token mint.
            recipient_token_account = get_associated_token_address(recipient_pubkey, token_mint_pubkey)

            # Build the token transfer instruction.
            transfer_instruction = transfer(
                TransferParams(
                    program_id=TOKEN_PROGRAM_ID,
                    source=sender_token_account,
                    dest=recipient_token_account,
                    owner=sender_pubkey,
                    amount=TOKEN_AMOUNT,
                )
            )

            # Create a new transaction and add the transfer instruction.
            txn = Transaction()
            txn.add(transfer_instruction)

            # Get a recent blockhash to include in the transaction.
            recent_blockhash_resp = client.get_recent_blockhash()
            recent_blockhash = (
                recent_blockhash_resp.get("result", {})
                .get("value", {})
                .get("blockhash")
            )
            if not recent_blockhash:
                logging.error("Failed to retrieve recent blockhash.")
                continue
            txn.recent_blockhash = recent_blockhash
            txn.fee_payer = sender_pubkey

            # Sign the transaction with the sender's keypair.
            txn_signed = txn.sign([sender])

            # For demonstration, we do not send the transaction.
            # In a production scenario, you would use:
            # tx_response = client.send_transaction(txn_signed, sender)
            # logging.info(f"Transaction sent: {tx_response}")

            logging.info(
                f"Simulated airdrop: {TOKEN_AMOUNT} tokens to {recipient_str} "
                f"(Recipient Token Account: {recipient_token_account})"
            )
        except Exception as e:
            logging.error(f"Error processing recipient {recipient_str}: {e}")


if __name__ == "__main__":
    simulate_airdrop()
