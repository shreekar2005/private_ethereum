// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PaymentNetwork {
    
    struct User {
        string userName;
        bool isRegistered;
    }

    // tracking registered users
    mapping(uint => User) public users;
    
    // checking if joint account exists between two users
    mapping(uint => mapping(uint => bool)) public jointAccounts;
    
    // tracking individual balance contribution on an edge
    // balances[A][B] means A's balance in the joint account with B
    mapping(uint => mapping(uint => uint)) public balances;

    // register a new user in the network
    function registerUser(uint _userId, string memory _userName) public {
        require(!users[_userId].isRegistered, "user already registered");
        users[_userId] = User(_userName, true);
    }

    // create a joint account and set individual balances
    function createAcc(uint _userId1, uint _userId2, uint _balance1, uint _balance2) public {
        require(users[_userId1].isRegistered && users[_userId2].isRegistered, "both users should be registered");
        require(!jointAccounts[_userId1][_userId2], "account already exists");

        jointAccounts[_userId1][_userId2] = true;
        jointAccounts[_userId2][_userId1] = true;

        balances[_userId1][_userId2] = _balance1;
        balances[_userId2][_userId1] = _balance2;
    }

    // transfer amount along the path
    function sendAmount(uint[] memory path, uint amount) public {
        require(path.length >= 2, "path should have at least sender and receiver");

        // first pass: check if all edges are there and have enough balance
        for (uint i = 0; i < path.length - 1; i++) {
            uint u = path[i];
            uint v = path[i+1];
            
            require(jointAccounts[u][v], "missing joint account in path");
            require(balances[u][v] >= amount, "insufficient balance on the edge");
        }

        // second pass: update the balances
        for (uint i = 0; i < path.length - 1; i++) {
            uint u = path[i];
            uint v = path[i+1];

            // deduct from sender side and add to receiver side
            balances[u][v] -= amount;
            balances[v][u] += amount;
        }
    }

    // close the joint account
    function closeAccount(uint _userId1, uint _userId2) public {
        require(jointAccounts[_userId1][_userId2], "account doesnt exist");

        jointAccounts[_userId1][_userId2] = false;
        jointAccounts[_userId2][_userId1] = false;

        balances[_userId1][_userId2] = 0;
        balances[_userId2][_userId1] = 0;
    }
}