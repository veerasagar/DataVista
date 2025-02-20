import { useState } from "react";
import axios from "axios";

const AddTransaction = ({ onTransactionAdded }) => {
  const [formData, setFormData] = useState({
    amount: "",
    category: "",
    type: "income",
    date: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/api/transactions", formData);
      if (response.status === 201) {
        onTransactionAdded(); // Refresh transactions list
        setFormData({ amount: "", category: "", type: "income", date: "" });
      }
    } catch (error) {
      console.error("Error adding transaction", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "20px" }}>
      <input type="number" name="amount" placeholder="Amount" value={formData.amount} onChange={handleChange} required />
      <input type="text" name="category" placeholder="Category" value={formData.category} onChange={handleChange} required />
      <select name="type" value={formData.type} onChange={handleChange}>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <input type="date" name="date" value={formData.date} onChange={handleChange} required />
      <button type="submit">Add Transaction</button>
    </form>
  );
};

export default AddTransaction;
