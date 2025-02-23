import React from 'react';
import {
  LineChart, BarChart, PieChart, ScatterChart, AreaChart,
  CartesianGrid, XAxis, YAxis, Tooltip, Legend, Line, Bar, Pie, Cell, Scatter, Area, ResponsiveContainer
} from 'recharts';

// Assuming COLORS is defined somewhere in your project
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const VisualizationChart = ({ data, visualization }) => {
  if (!data || !visualization) return null;

  const { chartType, configuration } = visualization;

  // Use the margin provided by the API or fall back to default values.
  const commonProps = {
    data,
    margin: configuration.margin || { top: 20, right: 30, left: 20, bottom: 20 }
  };

  // Convert tooltip formatter string into a function if provided.
  const tooltipFormatter = configuration.tooltip?.formatter
    ? eval(configuration.tooltip.formatter)
    : undefined;

  const renderChart = () => {
    switch (chartType.toLowerCase()) {
      case 'line':
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey={configuration.xAxis.dataKey}
              label={{ value: configuration.xAxis.label, position: 'insideBottom', offset: 0 }}
            />
            <YAxis />
            <Tooltip formatter={tooltipFormatter} />
            {configuration.legend && <Legend />}
            {configuration.lines?.map((line, index) => (
              <Line
                key={index}
                type="monotone"
                dataKey={line.dataKey}
                stroke={line.color || COLORS[index % COLORS.length]}
                dot={{ r: 4 }}
              />
            ))}
          </LineChart>
        );

      case 'bar':
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey={configuration.xAxis.dataKey}
              label={{ value: configuration.xAxis.label, position: 'insideBottom', offset: 0 }}
            />
            <YAxis />
            <Tooltip formatter={tooltipFormatter} />
            {configuration.legend && <Legend />}
            {configuration.bars?.map((bar, index) => (
              <Bar
                key={index}
                dataKey={bar.dataKey}
                fill={bar.color || COLORS[index % COLORS.length]}
              />
            ))}
          </BarChart>
        );

      case 'pie':
        return (
          <PieChart {...commonProps}>
            <Pie
              data={data}
              dataKey={configuration.valueKey}
              nameKey={configuration.nameKey}
              cx="50%"
              cy="50%"
              outerRadius={150}
              fill="#8884d8"
              label
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={tooltipFormatter} />
            {configuration.legend && <Legend />}
          </PieChart>
        );

      case 'scatter':
        return (
          <ScatterChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey={configuration.xAxis.dataKey}
              type="number"
              label={{ value: configuration.xAxis.label, position: 'insideBottom', offset: 0 }}
            />
            <YAxis
              dataKey={configuration.yAxis.dataKey}
              type="number"
              label={{ value: configuration.yAxis.label, angle: -90, position: 'insideLeft' }}
            />
            <Tooltip formatter={tooltipFormatter} cursor={{ strokeDasharray: '3 3' }} />
            {configuration.legend && <Legend />}
            <Scatter
              name={configuration.scatter.name}
              data={data}
              dataKey={configuration.scatter.dataKey}
              shape={configuration.scatter.shape}
              fill={configuration.scatter.fill}
            />
          </ScatterChart>
        );

      case 'area':
        return (
          <AreaChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey={configuration.xAxis.dataKey}
              label={{ value: configuration.xAxis.label, position: 'insideBottom', offset: 0 }}
            />
            <YAxis />
            <Tooltip formatter={tooltipFormatter} />
            {configuration.legend && <Legend />}
            {configuration.areas?.map((area, index) => (
              <Area
                key={index}
                type="monotone"
                dataKey={area.dataKey}
                fill={area.color || COLORS[index % COLORS.length]}
                stroke={area.stroke || COLORS[index % COLORS.length]}
              />
            ))}
          </AreaChart>
        );

      default:
        return null;
    }
  };

  return (
    <ResponsiveContainer width={configuration.width || "100%"} height={configuration.height || 400}>
      {renderChart()}
    </ResponsiveContainer>
  );
};

export default VisualizationChart;