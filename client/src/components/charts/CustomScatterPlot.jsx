import React from "react";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const CustomScatterPlot = ({ data, xKey, yKey }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
        <CartesianGrid />
        <XAxis type="number" dataKey={xKey} name="X" />
        <YAxis type="number" dataKey={yKey} name="Y" />
        <Tooltip cursor={{ strokeDasharray: "3 3" }} />
        <Scatter data={data} fill="#d72638" />
      </ScatterChart>
    </ResponsiveContainer>
  );
};

export default CustomScatterPlot;
