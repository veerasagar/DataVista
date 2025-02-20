const API_URL = "http://localhost:5000/transactions";

export const fetchTransactions = async () => {
  const response = await fetch(API_URL);
  return response.json();
};

export const addTransaction = async (transaction) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(transaction),
  });
  return response.json();
};
