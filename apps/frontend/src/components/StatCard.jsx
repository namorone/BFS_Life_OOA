export default function StatCard({ title, subtitle, value, variant = "" }) {
  return (
    <article className="stat-card">
      <h3>{title}</h3>
      <p className="stat-subtitle">{subtitle}</p>
      <strong
        className={`stat-value ${
          variant === "light"
            ? "light"
            : variant === "extra-light"
              ? "extra-light"
              : ""
        }`}
      >
        {value}
      </strong>
    </article>
  );
}