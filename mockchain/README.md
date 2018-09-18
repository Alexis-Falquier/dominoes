## Mock Blockchain and Concept CLI

For the concept, and an initial jumping off point we used a mock blockchain that is a typscript version of this tutorial:
https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

The full repo for the blockchain can be found in:
https://github.com/adamstaveley/testchain.git


### Building/Running the Typescript blockchain
Requires Node (developed using >= 8.4) and NPM (>= 5.3). You can manage Node/NPM versions with NVM.
TypeScript is part of the dependencies and will be installed locally.
```
$ git clone https://github.com/Alexis-Falquier/dominoes.git
$ cd mockchain/ts-main
```
- Install dependencies
```
$ npm install
```
- Run tests
```
$ sh bin/makeTest.sh
$ npm run build
$ npm test
```
- Run (will default to 8000 if no port specified)
```
$ npm start $PORT
```

You can run multiple nodes for this mockchain on a single server which is what our team did
You can link these nodes and comminucate with the chain using HTTP requests.

### Concept CLI
Built using Python3.5+
```
$ python3 demoCLI.py
```
The script will run a fully working concept CLI demonstratin how you would interract with our "blockchain".
The CLI demonstrates a basic demonstration of what the project sould be able to do when it is finalized.
Examples:
- add medical records to the ledger
- look up patient records by name
- look up records added by a specific provider
- see the state of the ledger

