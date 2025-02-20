import React, { useEffect, useState } from "react";
import Dashboard from "./components/Dashboard";

const App = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/transactions")
      .then((res) => res.json())
      .then((data) => setTransactions(data))
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return <Dashboard transactions={transactions} />;
};

export default App;
