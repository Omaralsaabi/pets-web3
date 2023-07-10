from solcx import compile_standard
import json
from web3 import Web3
from dotenv import load_dotenv
import os
from web3.exceptions import TransactionNotFound
from .models import ContractAddress

load_dotenv()


with open(
    "/home/omar/Desktop/Logatta/attpet/pet_registry_app/PetRegistry.sol", "r"
) as f:
    pet_registry_file = f.read()


# Compile the contract

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"PetRegistry.sol": {"content": pet_registry_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi",
                        "metadata",
                        "evm.bytecode",
                        "evm.sourceMap",
                    ]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open(
    "/home/omar/Desktop/Logatta/attpet/pet_registry_app/compiled_code.json", "w"
) as f:
    json.dump(compiled_sol, f)


# Get bytecode
bytecode = compiled_sol["contracts"]["PetRegistry.sol"]["PetRegistry"]["evm"][
    "bytecode"
]["object"]

# Get ABI
abi = compiled_sol["contracts"]["PetRegistry.sol"]["PetRegistry"]["abi"]

# For connecting to seplolia testnet
# infura_url = "https://sepolia.infura.io/v3/4227969b548343b68b6d3b8c347aad3f" # testnet
infura_url = "https://mainnet.infura.io/v3/4227969b548343b68b6d3b8c347aad3f"  # mainnet
w3 = Web3(Web3.HTTPProvider(infura_url))
# chain_id = 11155111 # testnet
chain_id = 1  # mainnet
my_address = "0x785E91f9E091b3D68C17Fea185E71135d6C0D438"
private_key = os.getenv("PRIVATE_KEY")
nonce = w3.eth.get_transaction_count(my_address)


# Create the contract in python


def deploy_contract():
    PetRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
    transaction = PetRegistry.constructor().build_transaction(
        {
            "from": my_address,
            "nonce": nonce,
            "chainId": chain_id,
            "gasPrice": w3.to_wei(13, "gwei"),
        }
    )
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    try:
        # Wait for the transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        # Check if the contract address is available in the receipt
        if tx_receipt.contractAddress is not None:
            contract_address = tx_receipt.contractAddress
            print("Contract deployed at:", contract_address)
            ContractAddress.objects.create(contract_address=contract_address)
            return contract_address
        else:
            print("Contract deployment failed.")
            return None

    except TransactionNotFound:
        print("Transaction not found. Please try again later.")

    return contract_address
