export default function MetricCard({ label, value }) {
  return (
    <div className="card">
      <p className="text-sm opacity-70">{label}</p>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  );
}
