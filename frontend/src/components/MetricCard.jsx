export default function MetricCard({ label, value, icon, color }) {
  return (
    <div className="glass-card metric-card">
      {icon && <span className="metric-icon" aria-hidden="true">{icon}</span>}
      <span className="metric-value" style={color ? { color } : undefined}>{value}</span>
      <span className="metric-label">{label}</span>
    </div>
  );
}
