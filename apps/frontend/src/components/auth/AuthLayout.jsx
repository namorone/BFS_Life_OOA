import "./auth.css";

function BrandHeader({ subtitle }) {
  return (
    <header className="auth-brand">
      <div className="auth-logo" aria-hidden="true">
        <svg
          className="auth-logo-icon"
          viewBox="0 0 32 36"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M16 2L4 9v18l12 7 12-7V9L16 2z"
            stroke="white"
            strokeWidth="2"
            strokeLinejoin="round"
          />
          <path d="M4 9l12 7 12-7" stroke="white" strokeWidth="2" />
          <path d="M16 16v18" stroke="white" strokeWidth="2" />
        </svg>
      </div>
      <h1 className="auth-app-title">Home Inventory &amp; Warranty Tracker</h1>
      <p className="auth-app-subtitle">{subtitle}</p>
    </header>
  );
}

export default function AuthLayout({ subtitle, children }) {
  return (
    <div className="auth-page">
      <div className="auth-shell">
        <BrandHeader subtitle={subtitle} />
        {children}
      </div>
    </div>
  );
}
