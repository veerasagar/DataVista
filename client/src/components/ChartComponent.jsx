import { PieChart, Pie, Tooltip, Cell } from "recharts";

const COLORS = ["#4CAF50", "#FF5252"];

const ChartComponent = ({ transactions }) => {
  const income = transactions.filter((t) => t.type === "income").reduce((acc, t) => acc + t.amount, 0);
  const expense = transactions.filter((t) => t.type === "expense").reduce((acc, t) => acc + t.amount, 0);

  const data = [
    { name: "Income", value: income },
    { name: "Expense", value: expense },
  ];

  return (
    <div>
      <h2>📈 Financial Overview</h2>
      <PieChart width={300} height={300}>
        <Pie data={data} cx="50%" cy="50%" outerRadius={100} fill="#8884d8" dataKey="value">
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
      <p><strong>Total Income:</strong> ${income}</p>
      <p><strong>Total Expense:</strong> ${expense}</p>
      <p><strong>Balance:</strong> ${income - expense}</p>
    </div>
  );
};

export default ChartComponent;
