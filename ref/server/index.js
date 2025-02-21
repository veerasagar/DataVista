import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import transactionRoutes from "./routes/transactions.js"; // Ensure this path is correct

const app = express();
app.use(express.json());
app.use(cors());

app.use("/transactions", transactionRoutes); // Ensure this is the correct endpoint

mongoose.connect("your-mongo-db-url", {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log("Connected to MongoDB");
    app.listen(5000, () => console.log("Server running on port 5000"));
}).catch(err => console.error("MongoDB connection error:", err));
