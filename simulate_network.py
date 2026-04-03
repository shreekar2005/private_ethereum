import json
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from web3 import Web3
import solcx

# installing solc 0.8.0
solcx.install_solc('0.8.0')

# connecting to local geth node on port 8545
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
print(f"Connected to Ethereum: {w3.is_connected()}")

# setting default account for paying gas fees
w3.eth.default_account = w3.eth.accounts[0]

# read and compile the solidity contract
with open("PaymentNetwork.sol", "r") as file:
    contract_source = file.read()

compiled_sol = solcx.compile_source(
    contract_source,
    output_values=['abi', 'bin'],
    solc_version='0.8.0'
)
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# deploying the contract
PaymentNetwork = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = PaymentNetwork.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
contract = w3.eth.contract(address=contract_address, abi=abi)
print(f"Contract Deployed at: {contract_address}")

# generating network with 100 users following power law
G = nx.barabasi_albert_graph(n=100, m=2)

print("Registering users and creating joint accounts...")
for node in G.nodes():
    # register each user
    contract.functions.registerUser(node, f"User_{node}").transact()

for u, v in G.edges():
    # setting combined balance using exponential distribution with mean 10
    combined_balance = int(np.random.exponential(scale=10))
    if combined_balance < 2:
        combined_balance = 2 # keeping at least 1 coin per user
        
    # distributing equally between both users
    balance_u = combined_balance // 2
    balance_v = combined_balance - balance_u
    
    contract.functions.createAcc(u, v, balance_u, balance_v).transact()

print("Network setup complete. Starting simulation...")

# simulating 1000 random transactions
success_rates = []
success_count = 0
total_transactions = 1000

for i in range(1, total_transactions + 1):
    sender = random.choice(list(G.nodes()))
    receiver = random.choice(list(G.nodes()))
    
    # making sure sender and receiver are different
    while receiver == sender:
        receiver = random.choice(list(G.nodes()))

    try:
        # finding shortest path (least hop count)
        path = nx.shortest_path(G, source=sender, target=receiver)
        
        # firing the transaction for 1 coin
        try:
            contract.functions.sendAmount(path, 1).transact()
            success_count += 1
        except Exception as e:
            # txn failed (mostly because of insufficient balance on some edge)
            pass
            
    except nx.NetworkXNoPath:
        pass

    # calculating ratio after every 100 txns
    if i % 100 == 0:
        ratio = success_count / i
        success_rates.append(ratio)
        print(f"Transactions: {i} | Success Ratio: {ratio:.4f}")

# plotting the graph
plt.plot(range(100, 1001, 100), success_rates, marker='o')
plt.xlabel("Number of Transactions")
plt.ylabel("Success Ratio")
plt.title("Transaction Success Ratio over Time")
plt.grid(True)
plt.show()