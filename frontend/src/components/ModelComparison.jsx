import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const METRICS = [
  { key: 'Accuracy', label: 'Accuracy', color: '#6366F1' },
  { key: 'Precision', label: 'Precision', color: '#8B5CF6' },
  { key: 'Recall', label: 'Recall', color: '#14B8A6' },
  { key: 'F1_Score', label: 'F1-Score', color: '#F43F5E' },
];

const shortName = (name = '') => {
  if (/logistic/i.test(name)) return 'Logistic';
  if (/naive/i.test(name)) return 'Naive Bayes';
  if (/svm/i.test(name)) return 'Linear SVM';
  return name;
};

export default function ModelComparison({ data }) {
  if (!data || data.length === 0) return <p style={{ color: 'var(--text-muted)' }}>No comparison data available.</p>;

  const chartData = data.map(d => ({
    name: d.Model,
    Accuracy: +(d.Accuracy * 100).toFixed(1),
    Precision: +(d.Precision * 100).toFixed(1),
    Recall: +(d.Recall * 100).toFixed(1),
    F1_Score: +(d.F1_Score * 100).toFixed(1),
  }));

  const best = {};
  METRICS.forEach(metric => {
    best[metric.key] = Math.max(...chartData.map(row => row[metric.key]));
  });

  return (
    <div>
      <h3 className="comparison-heading">Model Performance Comparison</h3>
      <p className="comparison-sub">Test-set scores across all classifiers. Higher is better.</p>

      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={330}>
          <BarChart
            data={chartData}
            barGap={3}
            barCategoryGap="26%"
            margin={{ top: 8, right: 8, left: -12, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
            <XAxis
              dataKey="name"
              tickFormatter={shortName}
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              interval={0}
            />
            <YAxis
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              tickFormatter={(value) => `${value}%`}
              axisLine={false}
              tickLine={false}
              width={48}
            />
            <Tooltip
              cursor={{ fill: 'rgba(124, 58, 237, .06)' }}
              contentStyle={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                borderRadius: 10,
                fontSize: '0.85rem',
              }}
              formatter={(value, name) => [`${value}%`, name]}
            />
            <Legend
              wrapperStyle={{ color: 'var(--text-secondary)', fontSize: 13, paddingTop: 10 }}
              iconType="circle"
              iconSize={9}
            />
            {METRICS.map(metric => (
              <Bar
                key={metric.key}
                dataKey={metric.key}
                name={metric.label}
                fill={metric.color}
                radius={[4, 4, 0, 0]}
                maxBarSize={22}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Comparison Table */}
      <div className="comparison-table-wrap">
        <table className="comparison-table">
          <thead>
            <tr>
              {['Model', ...METRICS.map(metric => metric.label)].map(heading => (
                <th key={heading}>{heading}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {chartData.map((row, i) => (
              <tr key={i}>
                <td className="comparison-model">{row.name}</td>
                {METRICS.map(metric => (
                  <td
                    key={metric.key}
                    className={`metric-cell${row[metric.key] === best[metric.key] ? ' is-best' : ''}`}
                  >
                    {row[metric.key]}%
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
