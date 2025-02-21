const Transactions = ({ transactions }) => {
  return (
    <div>
      <h2>📜 Transactions</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Amount</th>
            <th>Category</th>
            <th>Type</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {transactions.length > 0 ? (
            transactions.map((t) => (
              <tr key={t._id}>
                <td>${t.amount}</td>
                <td>{t.category}</td>
                <td>{t.type}</td>
                <td>{new Date(t.date).toLocaleDateString()}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4">No transactions found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Transactions;
