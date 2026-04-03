# Decentralized Payment Channel Network (DApp)

**Course:** CSL7490 - Blockchain Assignment 2  
**Development Environment:** This project was developed and tested natively on an **Ubuntu Linux** machine.

## Project Overview
This project implements a simplified Decentralized Application (DApp) acting as a Payment Channel Network on a private Ethereum blockchain. It utilizes a Solidity smart contract to manage joint accounts (edges) and user balances, and a Python script to generate a power-law network topology, deploy the contract, and simulate 1000 transactions to analyze success rates based on channel liquidity.

## File Structure
- `PaymentNetwork.sol`: The Solidity smart contract containing the core DApp logic (registering users, creating accounts, sending amounts).
- `simulate_network.py`: The Python script that interacts with the Geth node, deploys the contract, generates the 100-user power-law graph, and simulates transactions.
- `requirements.txt`: Contains the exact versions of the Python packages required to run the simulation.
- `data/`: The Geth database directory storing the persistent state of our local developer blockchain.
- `genesis.json`: Initial configuration file (Legacy, superseded by Geth's `--dev` mode).
- `LICENSE`: Project license file.
- `README.md`: Instructions for setup and execution.

## Prerequisites
To run this project, you must have a Linux/Ubuntu environment with the following installed:
1. **Go Ethereum (Geth)** (v1.17+)
2. **Python 3.10+**
3. **`venv`** (Python virtual environment module)

### 1. Install Geth (Ubuntu)
```bash
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
```

### 2. Set Up Python Virtual Environment & Install Dependencies
It is highly recommended to use a virtual environment to avoid polluting your global Python packages.
```bash
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages from requirements.txt
pip install -r requirements.txt
```

## Instructions for Compiling and Running

### Step 1: Start the Local Ethereum Node (Terminal 1)
We use Geth in Developer Mode (`--dev`) to create a localized, pre-funded Proof-of-Authority network. We utilize the `--datadir` flag to ensure the blockchain state persists between runs.

Open a terminal in the root directory of this project and run:
```bash
geth --dev --datadir ./data --http --http.api "eth,net,web3,personal" --http.corsdomain "*" --http.port 8545 console
```
*Note: Keep this terminal window open. You should see the Geth JavaScript console (`>`).*

### Step 2: Run the Simulation (Terminal 2)
The Python script handles the compilation of the Solidity contract via `py-solc-x`, deploys it using `web3.py`, and immediately begins the network simulation.

Open a **second terminal** in the same directory. Make sure you **activate the virtual environment** in this new terminal before running the script!
```bash
# Activate the venv in the new terminal
source .venv/bin/activate

# Run the simulation
python3 simulate_network.py
```

### Expected Output
1. The script will output the deployed contract address.
2. It will register 100 users and create edges with exponentially distributed balances.
3. It will fire 1,000 randomized transactions.
4. The terminal will print the success ratio every 100 transactions.
5. Finally, a `matplotlib` graph will appear displaying the transaction success ratio over time.

## Group Members

* (B23CS1069) b23cs1069@iitj.ac.in - Shreekar
* (B23CS1101) B23CS1101@iitj.ac.in - Tavishi Srivastava
* (B23CS1076) b23cs1076@iitj.ac.in - Vadlamudi Jyothsna
* (B23CS1031) b23cs1031@iitj.ac.in - Kurra Hema