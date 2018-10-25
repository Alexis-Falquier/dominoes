# DOMINOES BLOCKCHAIN

## About the Dominoes Chain

The blockchain built for this DePaul Senior Capstone project is built out specifically as a basic structure aiming to be a use case for a distributed ledger that keeps inmutable and verifiable medical records. This basic chain can run on multiple nodes and communicate with each of these. The structure of the chain is a basic single transaction block, where each block will hold a single medical record. The consensus method for the nodes is longest chain wins. It also incorperates a simple proof of work algorythm to try to mediate any two nodes attempting to write on the ledger at the same time.

The idea of the project is to demonstrate how we can leverage a blockchain in order to create an inmutable cannonical ledger for medical records.

## Dependencies
- Python 3
- Flask

## How to Run

This blockchain is built in a basic form to run on a single server on multiple ports, with a 'master' node set to be on port 5000. To run on different ports simply add the port number after the script name, otherwise it will spin up on port 5000. All new nodes automatically connect to the master node.

change directory to node1
to run in the background:
```
nohup python3 blockchain.py &
```
To run in foreground so you can see server logs:
```
python3 blockchain.py 
```
change directory to node2
to run in the background:
```
nohup python3 blockchain.py 5001 &
```
change directory to node3
to run in the background:
```
nohup python3 blockchain.py 5002 &
```
change directory to node4
to run in the background:
```
nohup python3 blockchain.py 5003 &
```

You now have a cluster of nodes running in ports 5000, 5001, 5002, and 5003. They are all connected and communicating, so any if you add records via node 5003, and then get the chain on node 5000, node 5000 will verify the chain and find that 5003 has the longest chain.

## Interacting With the Chain

The chain runs using flask, and you can interact with it using HTTP GET and POST requests. While if you look at the code there are various calls, there are only two that really matter:

GET
/verifiedchain
This call will return the correct state of the chain regardless of what node you call it from. Try it using curl on your command line (note: initially each node will have a different genesis block, once any node adds a record on the block that will be the correct chain and will now be inmutable):
```
curl -X GET http://127.0.0.1:5000/verifiedchain
```

POST
/addrecord
this call will add a new record on the block, whatever node it is called on will create the block do the work, verify it has the correct chain then add it to the chain. 
The format of medical records is a JSON format as such:

'{	
	"provider": "provider name",
	"providerID": "some id 123",
	"patient": "patient name",
	"patientID": "some id 456",
	"description": "what happened",
	"date": "1/1/18"
	}'
  
If you do not use this format, a record will not be added to the ledger. Try it using curl on your command line:
```
curl -X POST -H "Content-Type: application/json" -d '{"provider": "provider name", "providerID": "some id 123", "patient": "patient name", "patientID": "some id 456", "description": "what happened", "date": "1/1/18"	}' http://127.0.0.1:5000/newrecord
```

now try getting the chain from another node and see how it will have this record in the chain.

### References

The initial base of the chain is inspired from https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
