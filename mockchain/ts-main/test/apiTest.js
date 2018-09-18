const request = require('request-promise');
const assert = require('chai').assert;

require('../dist/index');

const options = {
    resolveWithFullResponse: true
}


describe('Basic API usage', () => {
    it('Should return 200 on GET /mine request', done => {
        const custom = {
            url: 'http://localhost:8000/mine', 
            method: 'GET'
        };
        request(Object.assign(custom, options)).then(res => {
            assert.equal(res.statusCode, 200);
            assert.property(JSON.parse(res.body), 'message');
            assert.property(JSON.parse(res.body), 'index');
            assert.property(JSON.parse(res.body), 'transactions');
            assert.property(JSON.parse(res.body), 'proof');
            assert.property(JSON.parse(res.body), 'previousHash');
            done();
        });
    });

    it('Should return 200 on GET /chain request', done => {
        const custom = {
            url: 'http://localhost:8000/chain', 
            method: 'GET'
        };
        request(Object.assign(custom, options)).then(res => {
            assert.equal(res.statusCode, 200);
            assert.property(JSON.parse(res.body), 'chain');
            assert.property(JSON.parse(res.body), 'length');     
            done();       
        });
    });

    it('Should return 200 and index on POST /transactions/new request', done => {

        const custom = {
            url: 'http://localhost:8000/transactions/new', 
            method: 'POST', 
            json: {
                sender: '123', 
                recipient: '456', 
                amount: 25
            }
        };
        request(Object.assign(custom, options)).then(res => {
            assert.equal(res.statusCode, 200);
            assert.property(res.body, 'message');
            done();
        });
    });
});


describe('Multipe node interactivity', () => {
    require('../dist/test/indexTest');

    it('Should return 200 on GET /nodes/register request', done => {
        const custom = {
            url: 'http://localhost:8001/nodes/register', 
            method: 'POST',
            json: {
                nodes: [
                    "http://127.0.0.1:8000"
                ]
            }
        }
        request(Object.assign(custom, options)).then(res => {
            assert.equal(res.statusCode, 200);
            assert.property(res.body, 'message');
            assert.property(res.body, 'totalNodes');
            done();    
        })
    });

    it('Should return 200 and updated chain on GET /nodes/resolve', done => {
        const custom = {
            url: 'http://localhost:8001/nodes/resolve',
            method: 'GET'
        }
        request(Object.assign(custom, options)).then(res => {
            assert.equal(res.statusCode, 200);
            assert.property(JSON.parse(res.body), 'newChain');
            done();
        })
    });
});