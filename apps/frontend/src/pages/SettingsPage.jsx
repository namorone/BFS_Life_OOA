import { useEffect, useState } from "react";
import "./SettingsPage.css";

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
    <div className="settings-layout">
      <aside className="settings-sidebar">
        <div className="sidebar-top">
          <h1 className="sidebar-title">Home Inventory</h1>
          <p className="sidebar-subtitle">Warranty Tracker</p>
        </div>

        <nav className="sidebar-nav">
          <a href="/" className="sidebar-link">Dashboard</a>
          <a href="#" className="sidebar-link">Notifications</a>
          <a href="#" className="sidebar-link">Profile</a>
          <a href="/settings" className="sidebar-link active">Settings</a>
        </nav>

        <div className="sidebar-bottom">
          <button className="logout-button">Logout</button>
        </div>
      </aside>

      <main className="settings-main">
        <div className="settings-header">
          <h2>Settings</h2>
          <p>Manage your application preferences</p>
        </div>

        <section className="settings-card">
          <div className="card-header">
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
              <span className="slider"></span>
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
              <span className="slider"></span>
            </label>
          </div>
        </section>

        <section className="settings-card">
          <div className="card-header">
            <h3>Account Settings</h3>
            <p>Manage your account security</p>
          </div>

          <div className="form-group">
            <label>Full Name</label>
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              name="email"
              value={form.email}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Preferred Currency</label>
            <select
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
          <div className="card-header">
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
              <span className="slider"></span>
            </label>
          </div>
        </section>

        <div className="settings-actions">
          <button className="save-button" onClick={handleSubmit}>
            Save Changes
          </button>
        </div>
      </main>
    </div>
  );
}
