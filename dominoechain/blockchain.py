import hashlib
import datetime
from flask import Flask, request
import json
import requests
import random
import sys

### DOMINOE MEDICAL RECORD BLOCKCHAIN ###

node = Flask(__name__)
# default port
PORT = 5000

# the basic structure of the blocks that make up the chain
# the block has: 
# an identifier id 
# creation timestamp (machine generated down to microseconds)
# medical_record: One medical record per block
# previous hash data: previous block hash used to hash this block thus permanently linking them
# hash: this blocks hash
# has function to create the block hash
class Block:
    def __init__(self, block_id, timestamp, data, previous_hash, replaced_hash):
        self.block_id = block_id
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        if replaced_hash != 0:
            self.hash = replaced_hash
        else:
            self.hash = self.blockHash()

    # inner function to create the block hash for each newly created block
    # uses sha256
    # hashes all the block information that makes up the block
    def blockHash(self):
        blockhash = hashlib.sha256()
        blockhash.update((
            str(self.block_id) + 
            str(self.timestamp) + 
            str(self.data) + 
            str(self.previous_hash)
            ).encode('utf-8'))
        return blockhash.hexdigest()




# the genesis or 'first' block that is created when the chain is initialized
# this contains nothing but an initial block to start the chain connected through their hashes
def createGenesisBlock():
  return Block(0, str(datetime.datetime.now()), "Genesis Block", 0, 0)




# This node's copy of the dominoe blockchain
blockchain = []
# initiate the blockchain
blockchain.append(createGenesisBlock())
# store information of other dominoe nodes
# this will be used for consensus on the correct chain
peer_nodes = []




@node.route('/newrecord', methods=['POST'])
def newRecord():
    # extract the medical record to be added to the chain
    new_record = request.get_json()
    # The record will be added to the chain
    # this will in turn mine a new block as well to ensure a single record block
    # log the records to the node console
    # since this calls all the required jason fields this in turn also acts
    # as a verification that the user inputed the record correctly
    # if json format is incorrect POST reqyest will fail
    print("New Record:")
    print("provider: %s" % new_record['provider'])
    print("providerID: %s" % new_record['providerID'])
    print("patient: %s" % new_record['patient'])
    print("patientID: %s" % new_record['patientID'])
    print("description: %s" % new_record['description'])
    print("date: %s" % new_record['date'])
    # mine the block with the new medical record
    new_block = mineNewBlock(new_record)
    # return block with record to client side
    return new_block




#@node.route('/mine', methods = ['GET'])
def mineNewBlock(new_record):
    # run consensus algo
    # this to ensure we have the correct chain so we can add the record
    # this way we don't lose records
    consensus()
    # get the last block on the chain
    last_block = blockchain[len(blockchain) - 1]
    # run proof of work to mine the block
    # currently no functional use, 
    # but can be useful as a potential hardware specific implementation
    # or in the future to add a reward system for mining
    powAlgo()
    # once the work is done we can mine the new block with the transaction
    new_block_data = {
        "provider": new_record['provider'],
        "providerID": new_record['providerID'],
        "patient": new_record['patient'],
        "patientID":new_record['patientID'],
        "description": new_record['description'],
        "date": new_record['date']
    }
    # generate new block meta data
    new_block_id = last_block.block_id + 1
    new_block_timestamp = str(datetime.datetime.now())
    last_block_hash = last_block.hash
    # generate block and add it to the chain
    mined_block = Block(
        new_block_id,
        new_block_timestamp,
        new_block_data,
        last_block_hash,
        0
    )
    blockchain.append(mined_block)
    # return mined block to client side
    return json.dumps({
        "blockID": new_block_id,
        "timestamp": new_block_timestamp,
        "data": new_block_data,
        "previous_hash": last_block_hash,
        "hash": last_block_hash
    }) + "\n"




# created a simple hash proof of work algo
def powAlgo():
    # loops until successfull
    # from random number 0-1000000000
    # if sha256 hash returns a hash ending in '00000' our work is successfull
    noProof = True
    while noProof:
        h = hashlib.sha256()
        h.update(str(random.randint(0,1000000000)).encode('utf-8'))
        if h.hexdigest()[-5:] == '00000':
            noProof = False




# longest chain wins consensus algorithm
def consensus():
    global blockchain
    # Get the chain states from the other nodes
    other_chains = getChains()
    # check which node has the longest chain
    longest_chain = blockchain
    chain_replaced = False
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            # if our chain was not the longest replace with the longest one
            longest_chain = chain
            chain_replaced = True
            print("longer chain found... replacing chain")
    # if there was a longer chain make the state of this chain the same as the longest one
    if chain_replaced:
        replaced_chain = []
        for correct_block in longest_chain:
            r_id = correct_block["blockID"]
            r_timestamp = correct_block["timestamp"]
            r_data = correct_block["data"]
            r_prev_hash = correct_block["previous_hash"]
            r_hash = correct_block["hash"]
            r_block = Block(
                r_id,
                r_timestamp,
                r_data,
                r_prev_hash,
                r_hash
            )
            replaced_chain.append(r_block)

        blockchain = replaced_chain
    return getChainState()




def getChains():
    # Get the blockchains from other nodes
    other_chains = []
    for node_url in peer_nodes:
        # make a list of the chains using a GET request
        try:
            block = requests.get(node_url + "/chainstate").content.decode('utf-8')
            block = json.loads(block)
            other_chains.append(block["dominoes_chain"])
        except:
            print("could not reach node in: " + str(node_url) )
    return other_chains




# GET request that will return the current state of the chain
@node.route('/chainstate', methods=['GET'])
def getChainState():
    # need to do this to maintain chain integrity
    chain = blockchain
    # iterate over every block
    # turn the blocks and chain into a json format to send to client side
    formated = []
    for i in range(len(chain)):
        block = chain[i]
        assembled = {
            "blockID": block.block_id,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        }
        formated.append(assembled)
    json_chain = json.dumps({
        "dominoes_chain": formated
    })
    return json_chain



# seperate GET request which will update the chain to make sure it is the verified one
# will replace chain if its not the longest and return the new verified state
@node.route('/verifiedchain', methods=['GET'])
def verifyChain():
    consensus()
    return getChainState()




# request to register a new node
@node.route('/registernode', methods=['POST'])
def newNode():
    global peer_nodes
    response = "failed"
    # get the node information from the json input
    node_info = request.get_json()
    new_node = str(node_info["node"])
    if (new_node not in peer_nodes):
        peer_nodes.append(new_node)
        response = "success"
    return "\nnode registration " + response




# when blockchain is initialized check if port option is given
# run either on default port or whichever is given
if __name__ == "__main__":
    # get the port from argument given
    argc= len( sys.argv )
    if argc > 2 :
	    sys.exit()
    if (argc == 2) :
        PORT = sys.argv[1]
        peer_nodes.append("http://127.0.0.1:5000")

# run the dominoe blockchain node on the selected port
node.run(port=PORT)
