import json
import solana
import time
import sys
import glob
import base64

import solana.system_program as sp

from solana.rpc.api import Client
from solana.blockhash import Blockhash
from solana.publickey import PublicKey

from solana.system_program import CreateAccountWithSeedParams, create_account_with_seed
from solana.transaction import Transaction, AccountMeta, TransactionInstruction

first_key_in_key_folder = glob.glob("keys/*")[0]
payer_loaded_account = solana.account.Account(json.load(open(first_key_in_key_folder))[:32])

deployed_program_key = glob.glob("dist/program/*")[0]
deployed_program_key_account = solana.account.Account(json.load(open(deployed_program_key))[:32])

http_client = Client("https://api.devnet.solana.com")
recent_blockhash = http_client.get_recent_blockhash()

payer_public_key = payer_loaded_account.public_key()
program_id = deployed_program_key_account.public_key()

GREETING_SEED = "hello"

tx = Transaction()
tx.recent_blockhash = Blockhash(recent_blockhash["result"]["value"]["blockhash"])

greeting_pubkey = PublicKey.create_with_seed(
    from_public_key=payer_public_key, seed=GREETING_SEED, program_id=program_id
)

print(f"Payer Account: {payer_public_key}")
print(f"Greeting Account: {greeting_pubkey}")

account_info = http_client.get_account_info(greeting_pubkey)
account_data = account_info.get("result").get("value").get("data")

account_greeting_count_data = account_data[0]

number_of_greetings = int.from_bytes(base64.b64decode(account_greeting_count_data), byteorder='little')

print(f"The account has been greeted {number_of_greetings} times!")