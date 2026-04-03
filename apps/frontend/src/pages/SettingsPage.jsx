import { useEffect, useState } from "react";

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
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async () => {
    await fetch("http://localhost:8000/api/v1/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    alert("Saved!");
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2>Settings</h2>

      <div>
        <label>Full Name</label>
        <br />
        <input name="full_name" value={form.full_name} onChange={handleChange} />
      </div>

      <div>
        <label>Email</label>
        <br />
        <input name="email" value={form.email} onChange={handleChange} />
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            name="notifications_enabled"
            checked={form.notifications_enabled}
            onChange={handleChange}
          />
          Notifications
        </label>
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            name="warranty_reminders_enabled"
            checked={form.warranty_reminders_enabled}
            onChange={handleChange}
          />
          Warranty reminders
        </label>
      </div>

      <div>
        <label>Currency</label>
        <br />
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

      <br />
      <button onClick={handleSubmit}>Save</button>
    </div>
  );
}
