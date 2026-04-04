import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import AuthLayout from "../components/auth/AuthLayout";
import { useAuth } from "../hooks/useAuth";
import { login as apiLogin } from "../services/api";

function safeReturnPath(raw) {
  if (!raw || typeof raw !== "string") return null;
  if (!raw.startsWith("/") || raw.startsWith("//")) return null;
  return raw;
}

export default function LoginPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      const next = safeReturnPath(searchParams.get("returnTo"));
      navigate(next || "/dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate, searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim() || !password) {
      setError("Please fill in all fields");
      return;
    }

    setSubmitting(true);
    try {
      const data = await apiLogin({ email: email.trim(), password });
      login(data);
      const next = safeReturnPath(searchParams.get("returnTo"));
      navigate(next || "/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthLayout subtitle="Manage your belongings with ease">
      <div className="auth-card">
        <div className="auth-card-header">
          <h2 className="auth-card-title">Login</h2>
          <p className="auth-card-desc">Enter your credentials to access your account</p>
        </div>

        {error ? <div className="auth-error">{error}</div> : null}

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          <div className="auth-field">
            <label className="auth-label" htmlFor="login-email">
              Email
            </label>
            <input
              id="login-email"
              className="auth-input"
              type="email"
              name="email"
              autoComplete="email"
              placeholder="your.email@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="auth-field">
            <label className="auth-label" htmlFor="login-password">
              Password
            </label>
            <input
              id="login-password"
              className="auth-input"
              type="password"
              name="password"
              autoComplete="current-password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="auth-submit" type="submit" disabled={submitting}>
            {submitting ? "Signing in…" : "Login"}
          </button>
        </form>

        <p className="auth-footer">
          Don&apos;t have an account?{" "}
          <Link className="auth-link" to="/register">
            Register here
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}
