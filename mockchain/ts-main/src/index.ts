import * as bodyParser from 'body-parser';
import * as express from 'express';
import * as morgan from 'morgan';
import * as uuid4 from 'uuid/v4';

import { Blockchain } from './blockchain';
import { Block, Transaction } from './types/custom';

const app = express();
app.use(bodyParser.json());
app.use(morgan('tiny'));

const port = parseInt(process.argv[process.argv.length - 1], 10) || 8000;

// generate globally unique address for this node
const nodeIdentifier = uuid4().replace(/-/g, '');

// instantiate blockchain
const blockchain = new Blockchain();

app.get('/mine', (req, res): void => {
    // run PoW algorithm to get next proof
    const lastBlock = blockchain.lastBlock;
    const lastProof = lastBlock.proof;
    const proof = blockchain.proofOfWork(lastProof);

    // receive reward for finding proof
    // sender 0 signifies that this node has mined new block
    const tx = { sender: '0', recipient: nodeIdentifier, amount: 1 };
    blockchain.newTransaction(tx);

    // forge new block by adding it to chain
    const block = blockchain.newBlock(proof);

    res.send({
        message: 'New block forged',
        index: block.index,
        transactions: block.transactions,
        proof: block.proof,
        previousHash: block.previousHash
    });
});

app.post('/transactions/new', (req, res): void => {
    const values: Transaction = req.body;

    // create new transaction
    const index = blockchain.newTransaction(values);

    res.send({
        message: `Transaction will be added to next block ${JSON.stringify(index)}`
    });
});

app.get('/chain', (req, res): void => {
    res.send({
        chain: blockchain.chain,
        length: blockchain.chain.length,
    });
});

app.post('/nodes/register', (req, res): void => {
    const nodes: string[] = req.body.nodes;

    if (!nodes) {
        res.status(400).send('Error: please supply valid list of nodes');
    }

    nodes.forEach((node: string) => blockchain.registerNode(node));

    res.send({
        message: 'New nodes have been added',
        totalNodes: JSON.stringify([...nodes])
    });
});

app.get('/nodes/resolve', async (req, res) => {
    const replaced = await blockchain.resolveConflicts();

    res.send(replaced
        ? {message: 'Chain was replaced', newChain: blockchain.chain}
        : {message: 'Chain remains authoritative', chain: blockchain.chain}
    );
});

app.listen(port);
