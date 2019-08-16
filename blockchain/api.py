import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source
from queuer.models import UserQueue
from blockchain.models import Contract

try:
    web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    web3.net.version
except ConnectionError as e:
    raise e

COINBASE = web3.eth.coinbase

def wait(tx, contract=False):
    # Wait for Transaction requested to the blockchain
    # Set contract to True if the transaction pending is a contract
    # deployment. Leave False if normal function/transaction call
    try:
        receipt = web3.eth.waitForTransactionReceipt(tx, timeout=60)
        timestamp = web3.eth.getBlock(receipt['blockNumber']).timestamp
        if receipt['status'] == 1:
            if contract:
                return receipt['contractAddress']

            else:
                return True, receipt['transactionHash'].hex(), timestamp
        else:
            return False, receipt['transactionHash'].hex(), timestamp

    except Exception as e:
        raise e


def save_contract(address, name, abi):
    # Save Contract template to DB
    # This stores the address and ABI of a contract template
    try:
        contract, created = Contract.objects.update_or_create(
            name=name,
            defaults={
                'address': address,
                'owner': web3.eth.coinbase,
                'abi': json.dumps(abi)})
        return contract

    except Exception as e:
        raise e


def deploy_contract(
        contract_source, contractName, constructorArgs=[], transactArgs={}):
    # If successful, returns Contract Address, and ABI

    with open(contract_source, 'r') as f:
        source = f.read()

    compiled_sol = compile_source(source)
    contract_interface = compiled_sol['<stdin>:%s' % contractName]

    Contract = web3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = Contract.constructor(*constructorArgs).transact(transactArgs)
    tx_receipt = wait(tx_hash, contract=True)

    return tx_receipt, contract_interface['abi']


def get_queue(address):
    try:
        cert = Contract.objects.get(name="Queue")
        abi = json.loads(cert.abi)

        QUEUE = web3.eth.contract(address=address, abi=abi)

        details = {
            'user': QUEUE.functions.user().call(),
            'queue_id': QUEUE.functions.queue_id().call(),
            'number': QUEUE.functions.number().call(),
            'valid': QUEUE.functions.valid().call()
        }
        return details

    except Exception as e:
        raise e


def create_queue(user_q):
    # Queue Factory
    conArgs = [COINBASE, user_q.user, user_q.queue_id, user_q.number]
    transArgs = {'from': COINBASE}

    try:
        queue, abi = deploy_contract(
            'blockchain/contracts/Certificate.sol',
            'Certificate', constructorArgs=conArgs, transactArgs=transArgs)

        return queue

    except Exception as e:
        raise e