// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PaymentNetwork {
    
    struct User {
        string userName;
        bool isRegistered;
    }

    // Tracks registered users
    mapping(uint => User) public users;
    
    // Tracks if an edge (joint account) exists between two user IDs
    mapping(uint => mapping(uint => bool)) public jointAccounts;
    
    // Tracks the individual balance contribution for a specific direction on an edge
    // balances[A][B] = A's balance in the joint account with B
    mapping(uint => mapping(uint => uint)) public balances;

    // Register a new user [cite: 71]
    function registerUser(uint _userId, string memory _userName) public {
        require(!users[_userId].isRegistered, "User is already registered.");
        users[_userId] = User(_userName, true);
    }

    // Create a joint account and set initial individual contributions [cite: 73]
    function createAcc(uint _userId1, uint _userId2, uint _balance1, uint _balance2) public {
        require(users[_userId1].isRegistered && users[_userId2].isRegistered, "Both users must be registered.");
        require(!jointAccounts[_userId1][_userId2], "Account already exists between these users.");

        jointAccounts[_userId1][_userId2] = true;
        jointAccounts[_userId2][_userId1] = true;

        balances[_userId1][_userId2] = _balance1;
        balances[_userId2][_userId1] = _balance2;
    }

    // Transfer amount along a specified path [cite: 75]
    function sendAmount(uint[] memory path, uint amount) public {
        require(path.length >= 2, "Path must contain at least a sender and receiver.");

        // PASS 1: Verification - ensure all edges exist and balances are sufficient [cite: 76, 77]
        for (uint i = 0; i < path.length - 1; i++) {
            uint u = path[i];
            uint v = path[i+1];
            
            require(jointAccounts[u][v], "Invalid path: missing joint account.");
            require(balances[u][v] >= amount, "Transaction Failed: Insufficient balance along the path.");
        }

        // PASS 2: Execution - update balances [cite: 22, 23, 24]
        for (uint i = 0; i < path.length - 1; i++) {
            uint u = path[i];
            uint v = path[i+1];

            // Decrease balance from sender's side, increase on receiver's side
            balances[u][v] -= amount;
            balances[v][u] += amount;
        }
    }

    // Terminate the account between two users [cite: 79, 80]
    function closeAccount(uint _userId1, uint _userId2) public {
        require(jointAccounts[_userId1][_userId2], "Account does not exist.");

        jointAccounts[_userId1][_userId2] = false;
        jointAccounts[_userId2][_userId1] = false;

        balances[_userId1][_userId2] = 0;
        balances[_userId2][_userId1] = 0;
    }
}
