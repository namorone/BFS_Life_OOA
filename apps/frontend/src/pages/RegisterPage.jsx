import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import AuthLayout from "../components/auth/AuthLayout";
import { useAuth } from "../hooks/useAuth";
import { register as apiRegister } from "../services/api";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!name.trim() || !email.trim() || !password || !confirmPassword) {
      setError("Please fill in all fields");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (!/[A-Za-z]/.test(password)) {
      setError("Password must contain at least one letter");
      return;
    }

    if (!/\d/.test(password)) {
      setError("Password must contain at least one digit");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setSubmitting(true);
    try {
      const data = await apiRegister({
        name: name.trim(),
        email: email.trim(),
        password,
      });
      login(data);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthLayout subtitle="Create your account to get started">
      <div className="auth-card">
        <div className="auth-card-header">
          <h2 className="auth-card-title">Register</h2>
          <p className="auth-card-desc">
            Create a new account to start tracking your inventory
          </p>
        </div>

        {error ? <div className="auth-error">{error}</div> : null}

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          <div className="auth-field">
            <label className="auth-label" htmlFor="register-name">
              Name
            </label>
            <input
              id="register-name"
              className="auth-input"
              type="text"
              name="name"
              autoComplete="name"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="auth-field">
            <label className="auth-label" htmlFor="register-email">
              Email
            </label>
            <input
              id="register-email"
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
            <label className="auth-label" htmlFor="register-password">
              Password
            </label>
            <input
              id="register-password"
              className="auth-input"
              type="password"
              name="password"
              autoComplete="new-password"
              placeholder="8+ chars, letter and number"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="auth-field">
            <label className="auth-label" htmlFor="register-confirm">
              Confirm Password
            </label>
            <input
              id="register-confirm"
              className="auth-input"
              type="password"
              name="confirmPassword"
              autoComplete="new-password"
              placeholder="Re-enter your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>

          <button className="auth-submit" type="submit" disabled={submitting}>
            {submitting ? "Creating account…" : "Register"}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{" "}
          <Link className="auth-link" to="/login">
            Login here
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}
