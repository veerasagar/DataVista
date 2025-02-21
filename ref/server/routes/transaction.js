import express from "express";
import Transaction from "../models/Transactions.js"; // Correct path

const router = express.Router();

// Get all transactions
router.get("/", async (req, res) => {
    try {
        const transactions = await Transaction.find();
        res.json(transactions);
    } catch (error) {
        console.error("Error fetching transactions:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

// Add a new transaction
router.post("/", async (req, res) => {
    try {
        const { amount, category, date, description } = req.body;
        const newTransaction = new Transaction({ amount, category, date, description });
        await newTransaction.save();
        res.status(201).json(newTransaction);
    } catch (error) {
        console.error("Error saving transaction:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

export default router;
