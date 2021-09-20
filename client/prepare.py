
import json
import solana
import time
import sys
import glob

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
account_info = account_info.get("result").get("value")

if account_info == None:
    print("Greeting Account Does Not Exist. Creating Now")
    # make dat account
    transaction_instruction = create_account_with_seed(
        params=CreateAccountWithSeedParams(
            from_pubkey=payer_public_key,
            new_account_pubkey=greeting_pubkey,
            base_pubkey=payer_public_key,
            seed={"length": len(GREETING_SEED), "chars": GREETING_SEED},
            lamports=10_000,
            space=4,
            program_id=program_id,
        )
    )
    tx.add(transaction_instruction)
    tx.sign(payer_loaded_account)

    http_client.simulate_transaction(tx)
    transaction_results = http_client.send_transaction(tx, payer_loaded_account)
    print(transaction_results)
else:
    print(f"Greeting Account Already Created")