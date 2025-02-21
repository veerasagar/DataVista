import { useEffect, useState } from "react";
import { fetchTransactions } from "../api";
import CustomLineChart from "../components/charts/CustomLineChart";
import CustomBarChart from "../components/charts/CustomBarChart";
import CustomPieChart from "../components/charts/CustomPieChart";
import CustomAreaChart from "../components/charts/CustomAreaChart";
import CustomScatterPlot from "../components/charts/CustomScatterPlot";
import AnimatedNumber from "../components/charts/AnimatedNumber";

const Dashboard = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const getData = async () => {
      const data = await fetchTransactions();
      setTransactions(data);
    };
    getData();
  }, []);

  return (
    <div>
      <h1>📊 Finance Dashboard</h1>
      {transactions.length === 0 ? (
        <p>📉 No transaction data available.</p>
      ) : (
        <>
          <AnimatedNumber transactions={transactions} />
          <CustomLineChart transactions={transactions} />
          <CustomBarChart transactions={transactions} />
          <CustomPieChart transactions={transactions} />
          <CustomAreaChart transactions={transactions} />
          <CustomScatterPlot transactions={transactions} />
        </>
      )}
    </div>
  );
};

export default Dashboard;
