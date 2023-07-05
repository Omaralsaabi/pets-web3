from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .deploy import (
    deploy_contract,
    abi,
    w3,
    my_address,
    chain_id,
    private_key,
)
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError
from .models import ContractAddress

# Create your views here


@api_view(["POST"])
def add_pet(request):
    pet_data = request.data

    if ContractAddress.objects.first():
        contract_address = ContractAddress.objects.first().contract_address
    else:
        contract_address = deploy_contract()
        ContractAddress.objects.create(contract_address=contract_address)

    contract = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(my_address)
    function = contract.functions.addPet(
        pet_data["name"],
        pet_data["kind"],
        pet_data["breed"],
        pet_data["color"],
        int(pet_data["age"]),
        pet_data["city"],
        pet_data["pet_address"],
        int(pet_data["phone"]),
        pet_data["ownerName"],
        pet_data["email"],
    )
    trasaction = function.build_transaction(
        {
            "from": my_address,
            "nonce": nonce,
            "chainId": chain_id,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(trasaction, private_key=private_key)
    raw_tx = signed_txn.rawTransaction

    tx_hash = w3.eth.send_raw_transaction(raw_tx)

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return Response({"message": "Pet added successfully"})


@api_view(["GET"])
def get_pet(request, pet_id):
    if ContractAddress.objects.first():
        contract_address = ContractAddress.objects.first().contract_address
    else:
        return Response({"message": "Contract does not exist"})

    contract = w3.eth.contract(address=contract_address, abi=abi)

    try:
        pet = contract.functions.getPet(pet_id).call()
        return Response({"pet": pet})
    except ContractLogicError as e:
        return Response({"message": "Pet does not exist"})
