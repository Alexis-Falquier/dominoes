const assert = require('chai').assert;

const Blockchain = require('../dist/blockchain').Blockchain;

const bc = new Blockchain();

describe('Mining', () => {
    it('Should mine new transactions', done => {
        const proof = bc.proofOfWork(bc.lastBlock.lastProof);
        const tx = {
            sender: '0',
            recipient: '1',
            amount: 1
        }
        bc.newTransaction(tx);
        const block = bc.newBlock(proof);

        assert.equal(block.index, bc.lastBlock.index);
        assert.equal(block.proof, proof);
        assert.property(block, 'transactions');
        assert.property(block, 'previousHash');
        assert.equal(block.transactions[0], tx);
        done();
    });
});

