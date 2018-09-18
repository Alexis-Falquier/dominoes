import * as crypto from 'crypto';
import * as url from 'url';

import * as request from 'request-promise';

import { Block, Transaction } from './types/custom';


export class Blockchain {
    /**
     * Creates a SHA-256 hash of a block
     */
    private static hash(block: Block): string {
        const blockString = JSON.stringify(block, Object.keys(block).sort());
        return crypto.createHash('sha256').update(blockString).digest('hex');
    }

    /**
     * Validates the proof: does hash(p, p') contain 4 leading zeros?
     */
    private static validProof(lastProof: number, proof: number): boolean {
        const guess = `${lastProof}${proof}`;
        const guessHash = crypto.createHash('sha256').update(guess).digest('hex');
        return guessHash.slice(-4) === '0000';
    }

    public chain: Block[];
    private currentTransactions: Transaction[];
    private nodes: Set<string>;

    constructor() {
        this.chain = [];
        this.currentTransactions = [];

        // create genesis block
        this.newBlock(100, '1');

        this.nodes = new Set();
    }

    public get lastBlock(): Block {
        return this.chain[this.chain.length - 1];
    }

    /**
     * Creates a new block in the Blockchain
     */
    public newBlock(proof: number, previousHash?: string): Block {
        const block = {
            index: this.chain.length + 1,
            timestamp: new Date().getTime(),
            transactions: this.currentTransactions,
            proof: proof,
            previousHash: previousHash || Blockchain.hash(this.lastBlock),
        };

        // reset current list of transactions
        this.currentTransactions = [];
        this.chain.push(block);
        return block;
    }

    /**
     * Creates a new transaction to go into the next mined block
     * Returns index of the block that will hold this transaction
     */
    public newTransaction(tx: Transaction): number {
        this.currentTransactions.push(tx);
        return this.chain.indexOf(this.lastBlock);
    }

    /**
     * Simple PoW algorithm:
     *  - find p' such that hash(pp') contains 4 leading zeros where p is previous p'
     */
    public proofOfWork(lastProof: number): number {
        let proof = 0;
        while (!Blockchain.validProof(lastProof, proof)) {
            proof += 1;
        }
        return proof;
    }

    /**
     * Add new node to list of known nodes
     */
    public registerNode(address: any): void {
        const parsedUrl = url.parse(address);
        this.nodes.add(parsedUrl.host);
        return;
    }

    /**
     * Consensus algorithm: replace chain with longest in network
     */
    public resolveConflicts(): Promise<boolean> {
        return new Promise((resolve, reject) => {
            // look for chains longer than current chain
            let maxLength = this.chain.length;
            let newChain: Block[];

            // verify chains from all nodes in network
            Array.from(this.nodes).forEach((node, index) => {
                const options = {
                    url: `http://${node}/chain`,
                    method: 'GET',
                    resolveWithFullResponse: true
                };

                request(options).then((res: any) => {
                    if (res.statusCode === 200) {
                        const body = JSON.parse(res.body);
                        const length = body.length;
                        const chain = body.chain;

                        if (length > maxLength && this.validChain(chain)) {
                            maxLength = length;
                            newChain = chain;
                        }

                        if (index === this.nodes.size - 1) {
                            if (newChain.length > this.chain.length) {
                                this.chain = newChain;
                                resolve(true);
                            } else {
                                resolve(false);
                            }
                        }
                    }
                });
            });
        });
    }

    /**
     * Determine if given blockchain is valid
     */
    private validChain(chain: Block[]): boolean {
        let lastBlock: Block = chain[0];
        let currentIndex = 1;

        while (currentIndex < chain.length) {
            const block: any = chain[currentIndex];
            console.log(lastBlock);
            console.log(block);
            console.log('\n----------\n');
            // check if hash of block is correct
            if (block.previousHash !== Blockchain.hash(lastBlock)) {
                return false;
            }
            // check PoW is correct
            if (!Blockchain.validProof(lastBlock.proof, block.proof)) {
                return false;
            }

            lastBlock = block;
            currentIndex += 1;
        }
        return true;
    }
}
