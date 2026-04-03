# Important Technical Learnings

This document summarizes the core architectural and conceptual learnings gathered during the development of the Decentralized Payment Channel Network.

## 1. Local Testing vs. Real Blockchain Infrastructure
* **The `--dev` Flag:** Instead of setting up a complex, multi-node Proof-of-Work/Stake network, Geth's `--dev` mode creates an ephemeral, single-node Proof-of-Authority testing lab. 
* **Networking is Disabled:** The node intentionally shuts off its P2P protocols (no `listen-address`, 0 peers) to isolate the testing environment from the global network.
* **On-Demand Mining:** In the real world, Ethereum mines blocks every 12 seconds. In `--dev` mode, the internal miner sleeps to save CPU and only wakes up to seal a block the exact millisecond a transaction enters the mempool.
* **Finality:** Blocks on a `--dev` network are never technically "finalized" because there are no other validators to vote on them. The `finalized block` count stays at 0, while the `head` block moves forward with every transaction.

## 2. World State and Contract Deployment
* **The World State:** This is the global cryptographic mapping of every address to its current balance, code, and storage data. Geth stores this as a Merkle Patricia Trie in a LevelDB/Pebble database on the hard drive.
* **Parallel Universes:** A smart contract is an isolated executable program. If the simulation script is run twice, it compiles and deploys *two* entirely separate instances of the contract to two different addresses. Contract B knows nothing about the state or users of Contract A, even though both exist simultaneously in the global World State.
* **Native Balance vs. Internal State:** The *native* Ethereum balance of our deployed contract is `0 ETH` because we didnt send real ETH during deployment. The "balances" we track in our Solidity code (`mapping(uint => mapping(uint => uint)) public balances`) are purely internal application variables simulating fake coins.

## 3. The Transaction Lifecycle: Verification vs. Execution
There is a strict boundary between verifying a transaction and executing its code.
* **Mempool Verification (No Code Execution):** When a transaction arrives at a node, the node *only* verifies the cryptography (the signature), the sequence (the nonce), and the sender's ability to pay gas. The EVM is NOT turned on, and no Solidity code runs. This prevents infinite-loop Denial of Service (DoS) attacks.
* **Execution (During Mining):** The chosen Block Proposer pulls the verified transaction from the mempool, spins up the EVM, runs the Solidity code, updates the World State, and packages it into a block.
* **Post-Execution (Network Consensus):** The Proposer broadcasts the block. Every other node receives it, spins up their own EVM, runs the exact same code, and verifies that their resulting State Root matches the Proposer's State Root.

## 4. Dry Runs (`eth_estimateGas`) vs. Real Transactions
* **The Sandbox:** Before sending a real transaction, `web3.py` sends an HTTP `eth_estimateGas` request. Geth spins up a temporary, read-only clone of the World State in RAM to simulate the transaction.
* **Why Nonces Dont Increase on Reverts:** If the simulated transaction hits a `require` statement that fails (e.g., "insufficient balance on the edge"), Geth throws away the temporary sandbox. The master World State is untouched, no gas is charged, and the account nonce does not increase.
* **Failed On-Chain Transactions:** If a transaction skips the dry run and fails *after* being mined into a real block by the Proposer, the World State *does* change. The sender's nonce increases, the gas fee is deducted from the sender, and that ETH is credited to the Block Proposer for their computational effort.

## 5. Network Topology and Edge Liquidity
* Our network uses a Barabási–Albert power-law graph with exponentially distributed balances. 
* In Payment Channel Networks (PCNs), edges act like physical pipes with limited capacity. Continuous transactions in a single direction rapidly drain the balance on the sender's side of the edge.
* When a crucial edge connecting to a central hub hits `0` balance in a specific direction, it acts as a severed artery, causing widespread routing failures and the steadily dropping success ratio observed in the simulation.