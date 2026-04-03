#!/bin/bash
geth --dev --datadir ./data --http --http.api "eth,net,web3,personal" --http.corsdomain "*" --http.port 8545 console