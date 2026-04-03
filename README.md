# Decentralized Payment Channel Network (DApp)

**Course:** CSL7490 - Blockchain Assignment 2  
**Development Environment:** This project was developed and tested natively on an **Ubuntu Linux** machine.

## Group Members
* (B23CS1069) b23cs1069@iitj.ac.in - Shreekar
* (B23CS1101) b23cs1101@iitj.ac.in - Tavishi Srivastava
* (B23CS1076) b23cs1076@iitj.ac.in - Vadlamudi Jyothsna
* (B23CS1031) b23cs1031@iitj.ac.in - Kurra Hema

## Project Overview
This project implements a simplified Decentralized Application (DApp) acting as a Payment Channel Network on a private Ethereum blockchain. It utilizes a Solidity smart contract to manage joint accounts (edges) and user balances, and a Python script to generate a 100-user power-law network topology, deploy the contract, and simulate 1000 transactions to analyze success rates based on channel liquidity.

## File Structure
- `PaymentNetwork.sol`: The Solidity smart contract containing the core DApp logic.
- `simulate_network.py`: The Python script that generates the graph, deploys the contract, and simulates the network transactions.
- `run_geth.sh`: Bash script to easily boot the local Geth developer node.
- `run_sim.sh`: Bash script to activate the virtual environment and run the Python simulation.
- `requirements.txt`: Contains the exact versions of the Python packages required to run the simulation.
- `data/`: The Geth database directory storing the persistent state of our local developer blockchain.
- `output_graph.png`: The generated plot of the transaction success ratio.
- `Blockchain_Assignment_2.pdf`: The original assignment requirements.
- `LICENSE` & `README.md`: Project documentation.

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
```bash
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages from requirements.txt
pip install -r requirements.txt
```

## Instructions for Compiling and Running

Make sure both bash scripts are executable before running them for the first time:
```bash
chmod +x run_geth.sh run_sim.sh
```

### Step 1: Start the Local Ethereum Node (Terminal 1)
We use Geth in Developer Mode (`--dev`) to create a localized, pre-funded Proof-of-Authority network. We utilize the `--datadir` flag to ensure the blockchain state persists between runs.

Open a terminal in the root directory and run:
```bash
./run_geth.sh
```
*Note: Keep this terminal window open. You should see the Geth JavaScript console (`>`).*

### Step 2: Run the Simulation (Terminal 2)
The Python script handles the compilation of the Solidity contract, deploys it, and immediately begins the network simulation.

Open a **second terminal** in the same directory and run:
```bash
./run_sim.sh
```

### Expected Output & Analysis
1. The script will output the deployed contract address.
2. It will register 100 users and create edges with combined balances following an exponential distribution (mean of 10), distributed equally.
3. It will fire 1,000 randomized 1-coin transactions.
4. The terminal will print the success ratio every 100 transactions, and a `matplotlib` graph will appear at the end.

**Why the graph looks the way it does:**
* **Initial Drop:** The Barabási–Albert graph relies on central "hubs." These highly connected nodes handle most of the traffic. Their edge balances drain rapidly in one direction, causing early transaction failures and a sharp drop in the success ratio.
* **The "Bump":** As transactions push liquidity heavily to one side of the network, massive balances accumulate on the receiving ends. Eventually, random transactions route back in the opposite direction, utilizing this pooled liquidity and causing a temporary spike in successful transactions.
* **Final Gridlock:** Over time, liquidity gets permanently trapped on the far edges of the network. The core hubs exhaust their two-way liquidity, leading to a steady decline in the success ratio as the network approaches gridlock.
