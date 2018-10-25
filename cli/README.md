# DOMINOES CLI

## TODO
- make it so you add node url as command line option (currently url hardocoded to my server)

This CLI will connect to your instance of the dominoes chain and will be an easy way to interract with it. This means you need to have at least one node running the chain. Go to the dominoechain directory and follow the instructions if you have not done this.

## How to Run
Simply start the script and provide the URL of one of your nodes so that it can connect and interact with your chain.
```
python3 CLI.py http://127.0.0.1:5000
```
You are now connected to your chain!

## Interacting With the Chain

This is a simplistic CLI with commands that will allow you to view records, by name, provider, or block ID. You can also view the entire chain should you so wish. Feel free to adapt the code to add even more functionality to the CLI.

The commands available are:

    help                        prints this menu
    addRecord                   add a new record to the ledger
    getRecordsByPatientName     prints records specific to a patient
    getRecordsByPatientID       prints records specific to a patient ID
    getRecordsByProvider        prints records made by a provider
    getRecordsByProviderID      prints records made by a provider ID
    getRecordByBlockID          prints the record of a specific block
    printLedger                 prints the entire ledger
    exit                        exits CLI

type 'help' at any time if you need reminding.
