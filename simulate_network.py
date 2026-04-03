import json
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from web3 import Web3
import solcx

# 1. Install specific solidity compiler version
solcx.install_solc('0.8.0')

# 2. Connect to local Ethereum node [cite: 81]
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
print(f"Connected to Ethereum: {w3.is_connected()}")

# Configure a default account for deploying and paying gas
w3.eth.default_account = w3.eth.accounts[0]

# 3. Compile the Solidity Contract
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

# Deploy Contract [cite: 83]
PaymentNetwork = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = PaymentNetwork.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
contract = w3.eth.contract(address=contract_address, abi=abi)
print(f"Contract Deployed at: {contract_address}")

# 4. Generate the Power-Law Network (100 users) [cite: 87]
# Using Barabasi-Albert model to ensure a connected graph with power-law degree distribution
G = nx.barabasi_albert_graph(n=100, m=2)

# 5. Register Users and Create Accounts
print("Registering users and creating joint accounts...")
for node in G.nodes():
    # Register user (using node integer as ID) [cite: 71]
    contract.functions.registerUser(node, f"User_{node}").transact()

for u, v in G.edges():
    # Combined balance follows exponential distribution with mean = 10 [cite: 88]
    combined_balance = int(np.random.exponential(scale=10))
    if combined_balance < 2:
        combined_balance = 2 # Ensure at least 1 coin each if an edge exists
        
    # Distributed equally [cite: 88]
    balance_u = combined_balance // 2
    balance_v = combined_balance - balance_u
    
    contract.functions.createAcc(u, v, balance_u, balance_v).transact()

print("Network setup complete. Starting simulation...")

# 6. Simulate Transactions [cite: 89, 90]
success_rates = []
success_count = 0
total_transactions = 1000

for i in range(1, total_transactions + 1):
    sender = random.choice(list(G.nodes()))
    receiver = random.choice(list(G.nodes()))
    
    # Ensure sender and receiver are different
    while receiver == sender:
        receiver = random.choice(list(G.nodes()))

    # Find shortest path using least hop count 
    try:
        # nx.shortest_path handles the BFS and resolves ties inherently by graph structure 
        path = nx.shortest_path(G, source=sender, target=receiver)
        
        # Fire transaction [cite: 84, 89]
        try:
            contract.functions.sendAmount(path, 1).transact()
            success_count += 1
        except Exception as e:
            # Transaction reverted (e.g., insufficient balance)
            pass
            
    except nx.NetworkXNoPath:
        # Should not happen as barabasi_albert generates connected graphs, but good practice
        pass

    # Report and store data every 100 transactions [cite: 90]
    if i % 100 == 0:
        ratio = success_count / i
        success_rates.append(ratio)
        print(f"Transactions: {i} | Success Ratio: {ratio:.4f}")

# 7. Plotting the results [cite: 90]
plt.plot(range(100, 1001, 100), success_rates, marker='o')
plt.xlabel("Number of Transactions")
plt.ylabel("Success Ratio")
plt.title("Transaction Success Ratio over Time")
plt.grid(True)
plt.show()