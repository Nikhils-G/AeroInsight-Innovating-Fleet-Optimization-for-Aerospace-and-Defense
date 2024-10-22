import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Plane, Fuel, AlertTriangle, Clock, TrendingUp, Boxes } from 'lucide-react';

// Simulated data generation with predictive elements
const generateData = (length) => {
  let maintenanceScore = 100;
  let fuelEfficiency = 95;
  let fleetSize = 25;
  return Array.from({ length }, (_, i) => {
    maintenanceScore -= Math.random() * 2;
    fuelEfficiency -= Math.random() * 0.5;
    return {
      time: i,
      fuelEfficiency: fuelEfficiency,
      maintenanceScore: maintenanceScore,
      predictedMaintenanceDate: maintenanceScore < 80 ? i + Math.floor(Math.random() * 10) : null,
      flightDelay: Math.random() * 30,
      supplyChainDelay: Math.random() * 5,
      predictedFuelEfficiency: fuelEfficiency - (Math.random() * 2),
      fleetSize: fleetSize,
    };
  });
};

// Improved Card component with more visual elements
const Card = ({ title, value, icon, trend, trendValue }) => (
  <div className="bg-white rounded-lg shadow-md p-4">
    <div className="flex items-center justify-between mb-2">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      {icon}
    </div>
    <div className="flex items-center justify-between">
      <p className="text-2xl font-bold">{value}</p>
      <div className={flex items-center ${trend === 'up' ? 'text-green-500' : 'text-red-500'}}>
        {trend === 'up' ? <TrendingUp className="h-5 w-5 mr-1" /> : <TrendingUp className="h-5 w-5 mr-1 rotate-180" />}
        <span className="text-sm font-medium">{trendValue}</span>
      </div>
    </div>
  </div>
);

// Improved Chart component with more customization options
const Chart = ({ title, data, dataKey, color, type = 'line', height = 300 }) => (
  <div className="bg-white rounded-lg shadow-md p-4">
    <h3 className="text-lg font-semibold mb-4">{title}</h3>
    <ResponsiveContainer width="100%" height={height}>
      {type === 'line' ? (
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey={dataKey} stroke={color} />
        </LineChart>
      ) : (
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={dataKey} fill={color} />
        </BarChart>
      )}
    </ResponsiveContainer>
  </div>
);

// Improved Predictive Maintenance component with more visual cues
const PredictiveMaintenance = ({ data }) => {
  const maintenanceNeeded = data.filter(d => d.predictedMaintenanceDate !== null);

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <h3 className="text-lg font-semibold mb-4">Predictive Maintenance</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={maintenanceNeeded}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="predictedMaintenanceDate" fill="#8884d8" />
          <Bar dataKey="maintenanceScore" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// Improved Supply Chain Delays component with more visual elements
const SupplyChainDelays = ({ data }) => (
  <div className="bg-white rounded-lg shadow-md p-4">
    <h3 className="text-lg font-semibold mb-4">Supply Chain Delays</h3>
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="supplyChainDelay" stroke="#82ca9d" />
        <Line type="monotone" dataKey="flightDelay" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

// Improved Fleet Optimization Recommendations component with more visual elements
const FleetOptimizationRecommendations = () => (
  <div className="bg-white rounded-lg shadow-md p-4">
    <h3 className="text-lg font-semibold mb-4">Fleet Optimization Recommendations</h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-blue-50 rounded-lg p-4">
        <div className="flex items-center mb-2">
          <Boxes className="h-6 w-6 text-blue-500 mr-2" />
          <h4 className="text-lg font-semibold">Maintenance Needed</h4>
        </div>
        <ul className="list-disc pl-5">
          <li>Schedule maintenance for Aircraft #5 within the next 7 days</li>
          <li>Consider retiring Aircraft #8 due to recurring maintenance issues</li>
        </ul>
      </div>
      <div className="bg-green-50 rounded-lg p-4">
        <div className="flex items-center mb-2">
          <TrendingUp className="h-6 w-6 text-green-500 mr-2" />
          <h4 className="text-lg font-semibold">Fuel Efficiency Improvements</h4>
        </div>
        <ul className="list-disc pl-5">
          <li>Optimize flight routes for Aircraft #12 to improve fuel efficiency</li>
          <li>Implement new fuel management system on Aircraft #3, #7, and #9</li>
        </ul>
      </div>
    </div>
  </div>
);

// Improved Main Dashboard component with more visual elements and dynamic updates
const AerospaceAnalyticsDashboard = () => {
  const [data, setData] = useState(generateData(30));

  useEffect(() => {
    const interval = setInterval(() => {
      setData(prevData => {
        const newData = [...prevData.slice(1), generateData(1)[0]];
        newData[newData.length - 1].time = prevData[prevData.length - 1].time + 1;
        return newData;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8 text-center text-blue-600">Aerospace Analytics Platform</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card title="Fleet Size" value={data[data.length - 1].fleetSize} icon={<Plane className="h-6 w-6 text-blue-500" />} trend="up" trendValue="5%" />
        <Card title="Avg. Fuel Efficiency" value={${data[data.length - 1].fuelEfficiency.toFixed(2)}%} icon={<Fuel className="h-6 w-6 text-green-500" />} trend="up" trendValue="2.5%" />
        <Card title="Maintenance Alerts" value={data.filter(d => d.maintenanceScore < 80).length} icon={<AlertTriangle className="h-6 w-6 text-red-500" />} trend="down" trendValue="10%" />
        <Card title="Avg. Flight Delay" value={${(data.reduce((sum, d) => sum + d.flightDelay, 0) / data.length).toFixed(2)} min} icon={<Clock className="h-6 w-6 text-yellow-500" />} trend="down" trendValue="5%" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Chart title="Fuel Efficiency Trend" data={data} dataKey="fuelEfficiency" color="#8884d8" />
        <Chart title="Maintenance Score" data={data} dataKey="maintenanceScore" color="#82ca9d" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <PredictiveMaintenance data={data} />
        <SupplyChainDelays data={data} />
      </div>

      <div className="grid grid-cols-1 gap-6">
        <FleetOptimizationRecommendations />
      </div>
    </div>
  );
};

// App component
const App = () => (
  <>
    <AerospaceAnalyticsDashboard />
  </>
);

export default App;