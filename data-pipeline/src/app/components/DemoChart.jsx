// pages/my-page.jsx or a component
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const DemoChart = () => {
  return (
    <div>
      <h1>My Chart Page</h1>
      <Plot
        data={[
          {
            x: [1, 2, 3],
            y: [2, 6, 3],
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: 'red'}
          },
          {
            type: 'bar',
            x: [1, 2, 3],
            y: [2, 5, 3]
          }
        ]}
        layout={ {width: 320, height: 240, title: {text: 'A Fancy Plot'}} }
        useResizeHandler={true}
        style={{ width: '50%', height: '50%' }}
      />
    </div>
  );
};

export default DemoChart;
