import mongoose from "mongoose";

const TransactionSchema = new mongoose.Schema({
    amount: {
        type: Number,
        required: true
    },
    category: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        default: Date.now
    },
    description: {
        type: String
    }
});

const Transaction = mongoose.model("Transaction", TransactionSchema);
export default Transaction;
