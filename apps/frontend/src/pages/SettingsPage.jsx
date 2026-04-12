import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import "./SettingsPage.css";
import "../styles/dashboard.css";

export default function SettingsPage() {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    notifications_enabled: true,
    warranty_reminders_enabled: true,
    preferred_currency: "USD",
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/settings")
      .then((res) => res.json())
      .then((data) => {
        setForm(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load settings:", err);
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async () => {
    try {
      await fetch("http://localhost:8000/api/v1/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      alert("Saved!");
    } catch (err) {
      console.error("Failed to save settings:", err);
      alert("Failed to save settings");
    }
  };

  if (loading) return <div className="settings-loading">Loading...</div>;

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-main">
        <div className="settings-header-block">
          <h1 className="settings-title">Settings</h1>
          <p className="settings-subtitle">Manage your application preferences</p>
        </div>

        <section className="settings-card">
          <div className="settings-card-header">
            <h3>Notification Preferences</h3>
            <p>Configure how you receive notifications</p>
          </div>

          <div className="settings-row">
            <div>
              <div className="settings-row-title">Email Notifications</div>
              <div className="settings-row-description">
                Receive email updates about your inventory
              </div>
            </div>

            <label className="switch">
              <input
                type="checkbox"
                name="notifications_enabled"
                checked={form.notifications_enabled}
                onChange={handleChange}
              />
              <span className="slider" />
            </label>
          </div>

          <div className="settings-row">
            <div>
              <div className="settings-row-title">Warranty Expiration Alerts</div>
              <div className="settings-row-description">
                Get notified when warranties are expiring
              </div>
            </div>

            <label className="switch">
              <input
                type="checkbox"
                name="warranty_reminders_enabled"
                checked={form.warranty_reminders_enabled}
                onChange={handleChange}
              />
              <span className="slider" />
            </label>
          </div>
        </section>

        <section className="settings-card">
          <div className="settings-card-header">
            <h3>Account Settings</h3>
            <p>Manage your account security</p>
          </div>

          <div className="settings-form-group">
            <label htmlFor="full_name">Full Name</label>
            <input
              id="full_name"
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
            />
          </div>

          <div className="settings-form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              value={form.email}
              onChange={handleChange}
            />
          </div>

          <div className="settings-form-group">
            <label htmlFor="preferred_currency">Preferred Currency</label>
            <select
              id="preferred_currency"
              name="preferred_currency"
              value={form.preferred_currency}
              onChange={handleChange}
            >
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="UAH">UAH</option>
            </select>
          </div>
        </section>

        <section className="settings-card">
          <div className="settings-card-header">
            <h3>Appearance</h3>
            <p>Customize how the app looks</p>
          </div>

          <div className="settings-row">
            <div>
              <div className="settings-row-title">Dark Mode</div>
              <div className="settings-row-description">
                Toggle dark mode theme
              </div>
            </div>

            <label className="switch disabled-switch">
              <input type="checkbox" disabled />
              <span className="slider" />
            </label>
          </div>
        </section>

        <section className="settings-card">
          <div className="settings-card-header">
            <h3>Category Management</h3>
            <p>Organize your inventory with custom categories</p>
          </div>

          <div className="settings-card-actions">
            <Link to="/categories" className="settings-link-button">
              Manage Categories
            </Link>
          </div>
        </section>

        <div className="settings-page-actions">
          <button className="primary-button" onClick={handleSubmit}>
            Save Changes
          </button>
        </div>
      </main>
    </div>
  );
}
