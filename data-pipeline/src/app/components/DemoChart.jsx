// pages/my-page.jsx or a component
import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function DemoChart() {
  const [data, setData] = useState({ bitcoin: [], ethereum: [] });
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8001/data/history?limit=100');
      const json = await res.json();
      
      const bitcoinData = json.filter(d => d.asset === 'bitcoin').map(d => ({ x: d.timestamp, y: d.price }));
      const ethereumData = json.filter(d => d.asset === 'ethereum').map(d => ({ x: d.timestamp, y: d.price }));

      setData({
        bitcoin: {
          x: bitcoinData.map(d => d.x),
          y: bitcoinData.map(d => d.y),
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Bitcoin'
        },
        ethereum: {
          x: ethereumData.map(d => d.x),
          y: ethereumData.map(d => d.y),
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Ethereum'
        }
      });
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // fetch every 10 seconds
    return () => clearInterval(interval);
  }, []);
  
  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>My Chart Page</h1>
      <Plot
        data={[data.bitcoin]}
        layout={{ 
          width: 800, 
          height: 600, 
          title: { title: 'Crypto Prices' },
          xaxis: { title: { text: 'Timestamp' } },
          yaxis: { title: { text: 'Price (USD)' } }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
};
