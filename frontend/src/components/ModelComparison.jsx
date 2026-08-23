import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const COLORS = ['#6366f1', '#14b8a6', '#f43f5e'];

export default function ModelComparison({ data }) {
  if (!data || data.length === 0) return <p style={{ color: 'var(--text-muted)' }}>No comparison data available.</p>;

  const chartData = data.map(d => ({
    name: d.Model,
    Accuracy: +(d.Accuracy * 100).toFixed(1),
    Precision: +(d.Precision * 100).toFixed(1),
    Recall: +(d.Recall * 100).toFixed(1),
    F1_Score: +(d.F1_Score * 100).toFixed(1),
  }));

  return (
    <div>
      <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: 16 }}>
        Model Performance Comparison
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} barCategoryGap="20%">
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
          <XAxis dataKey="name" tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-color)',
              borderRadius: 8,
              fontSize: '0.85rem',
            }}
          />
          <Bar dataKey="F1_Score" name="F1-Score" radius={[4, 4, 0, 0]}>
            {chartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Comparison Table */}
      <div style={{ overflowX: 'auto', marginTop: 20 }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontSize: '0.88rem',
        }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--border-color)' }}>
              {['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score'].map(h => (
                <th key={h} style={{
                  padding: '10px 12px',
                  textAlign: 'left',
                  color: 'var(--text-secondary)',
                  fontWeight: 600,
                  fontSize: '0.82rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em',
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {chartData.map((row, i) => (
              <tr key={i} style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '10px 12px', fontWeight: 600 }}>{row.name}</td>
                <td style={{ padding: '10px 12px' }}>{row.Accuracy}%</td>
                <td style={{ padding: '10px 12px' }}>{row.Precision}%</td>
                <td style={{ padding: '10px 12px' }}>{row.Recall}%</td>
                <td style={{ padding: '10px 12px', fontWeight: 700, color: COLORS[i % COLORS.length] }}>{row.F1_Score}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
