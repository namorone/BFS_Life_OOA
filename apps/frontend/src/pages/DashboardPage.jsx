import { useEffect, useState } from "react";

import AddItemModal from "../components/AddItemModal";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import Toast from "../components/Toast";
import { createItem, fetchCategories, fetchDashboardStats } from "../services/api";
import "../styles/dashboard.css";

const defaultStats = {
  total_items: 0,
  active_warranties: 0,
  expiring_soon: 0,
};

export default function DashboardPage() {
  const [stats, setStats] = useState(defaultStats);
  const [categories, setCategories] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [toast, setToast] = useState({
    visible: false,
    message: "",
    type: "success",
  });

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const [statsData, categoriesData] = await Promise.all([
          fetchDashboardStats(),
          fetchCategories(),
        ]);

        setStats(statsData);
        setCategories(categoriesData);
      } catch (loadError) {
        setError(loadError.message || "Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const showToast = (message, type = "success") => {
    setToast({
      visible: true,
      message,
      type,
    });
  };

  const hideToast = () => {
    setToast({
      visible: false,
      message: "",
      type: "success",
    });
  };

  const handleSaveItem = async (form) => {
    setSaving(true);
    setError("");

    try {
      await createItem(form);
      const freshStats = await fetchDashboardStats();
      setStats(freshStats);
      setModalOpen(false);
      showToast("Item saved successfully", "success");
    } catch (saveError) {
      const message = saveError.message || "Failed to save item";
      setError(message);
      showToast(message, "error");
      throw saveError;
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <div className="dashboard-layout">
        <Sidebar />

        <main className="dashboard-main">
          <div className="dashboard-header">
            <h1 className="dashboard-page-title">Dashboard</h1>
            <p className="dashboard-page-subtitle">
              Welcome to your Home Inventory & Warranty Tracker
            </p>
          </div>

          {error ? <div className="banner error">{error}</div> : null}

          <section className="stats-grid">
            <StatCard
              title="Total Items"
              subtitle="Items in your inventory"
              value={loading ? "..." : stats.total_items}
            />
            <StatCard
              title="Active Warranties"
              subtitle="Currently valid warranties"
              value={loading ? "..." : stats.active_warranties}
              variant="light"
            />
            <StatCard
              title="Expiring Soon"
              subtitle="Warranties expiring this month"
              value={loading ? "..." : stats.expiring_soon}
              variant="extra-light"
            />
          </section>

          <section className="quick-actions-card">
            <div>
              <h3 className="quick-actions-title">Quick Actions</h3>
              <p className="quick-actions-subtitle">
                Get started with your inventory management
              </p>
            </div>

            <div className="quick-actions-row">
              <button
                type="button"
                className="primary-button action-button"
                onClick={() => setModalOpen(true)}
              >
                <span className="action-button-icon">+</span>
                <span>Add Item</span>
              </button>

              <button type="button" className="primary-button action-button secondary-tone">
                <span className="action-button-icon">+</span>
                <span>Add Repair</span>
              </button>
            </div>
          </section>
        </main>

        <AddItemModal
          open={modalOpen}
          categories={categories}
          saving={saving}
          onClose={() => setModalOpen(false)}
          onSave={handleSaveItem}
        />
      </div>

      <Toast
        visible={toast.visible}
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
      />
    </>
  );
}