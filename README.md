## Hello World Solana + Python

This repo is a simple "Hello World" Solana program. We'll compile, deploy and then interact with the program using small Python3 scripts.

This example is basically a copy of https://github.com/solana-labs/example-helloworld but the client uses Python instead of Typescript.

This repo aims to be a simple step by step example of Solana for Python developers. 

You should be able to copy and paste your way through this full example and interact with a live Solana program on devnet. Please open an issue if you have any issues deploying the examples using the instructions below.  

🚀

# Program Deployment

Get repo. 

```bash
git clone https://github.com/drbh/solana-helloworld-py.git
cd solana-helloworld-py

# add folders we'll use in the example
mkdir keys # for our private key file
mkdir dist # for the compiled program
```

Make a key pair for deployment.

```bash
cd keys
solana-keygen grind --starts-with "dev:1"
# Wrote keypair to devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E.json
```

Set network. 

```bash
# set network
solana config set --url https://api.devnet.solana.com
```

Fund account for transactions (deploy, interact). 

```bash
solana airdrop 10 devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E
```

Compile Rust code to program. 

```bash
cd .. # solana-helloworld-py
cargo build-bpf --bpf-out-dir=dist/program

# dist/program
# ├── helloworldpy-keypair.json
# └── helloworldpy.so

# 0 directories, 2 files
```

Deploy program using the keys we made. 

```bash
solana program deploy dist/program/helloworldpy.so \
  --keypair keys/devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E.json

# Program Id: 8mUvuC4X3EUBq6bS75Z9FR14hpRw7VWQ3ibnRRTedHFR
```

# Interacting with Program


We can see our payer account and the PDA (Program Derived Account) using the first script. Note that this PDA has not been created - we've just calculated it's address at this point.

```bash
python3 client/accounts.py
# Payer Account: devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E
# Greeting Account: PfVawx2VXk1vVGQYRgPebFLG8uqY7eHRfWQj5WkP4bm
```

Now we can create the PDA by funding this account on the network. This is done with a special command. It's important to understand why we'll need this account created.

Since Solana programs are stateless they need a location to store user specific state. This can be done using a PDA address that links the program with the payer account. In this step we create this account.

```bash
python3 client/prepare.py
# Payer Account: devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E
# Greeting Account: PfVawx2VXk1vVGQYRgPebFLG8uqY7eHRfWQj5WkP4bm
# Greeting Account Does Not Exist. Creating Now
# {'jsonrpc': '2.0', 'result': 'KyDa5AZ2s43YTqubvmTvY8UK84amq9GTTL2iCbJZgKksrwL9SrUZrtwNWVahhc9kvDoFDzZJdqVqKNZwSytvucM', 'id': 5}
```

Lets use the actual program! We'll call this script which should update the data stored in the PDA account.  

```bash
python3 client/greet.py
# Payer Account: devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E
# Greeting Account: PfVawx2VXk1vVGQYRgPebFLG8uqY7eHRfWQj5WkP4bm
# {'jsonrpc': '2.0', 'result': '2oMnR66MZjhW4cYdzvjieUBwdXFWF6AuMTuvBAPYWX4MoiZydN18zfcFbM1347WPyiNbD9AbUFKwfzDvQW688e7Q', 'id': 4}
```

We can read the values from the program with the next script! *Remember we'll only see updates after they've been FULLY confirmed - this could take a couple of seconds*

```bash
python3 client/read.py
# Payer Account: devnF81ktubYxQRvmuvTUh71MAViSRa3xVsGeD1mm6E
# Greeting Account: PfVawx2VXk1vVGQYRgPebFLG8uqY7eHRfWQj5WkP4bm
# The account has been greeted 2 times!
```
