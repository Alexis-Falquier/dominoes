export interface Block {
    index: number;
    timestamp: number;
    transactions: any[];
    proof: number;
    previousHash: string;
}

export interface Transaction {
    sender: string;
    recipient: string;
    amount: number;
}
