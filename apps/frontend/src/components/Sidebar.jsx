import {
  Bell,
  Box,
  LayoutDashboard,
  LogOut,
  Settings,
  User,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, to: "/dashboard" },
  { label: "Inventory", icon: Box, to: "/inventory" },
  { label: "Notifications", icon: Bell, to: "/notifications" },
  { label: "Profile", icon: User, to: "/profile" },
  { label: "Settings", icon: Settings, to: "/settings" },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <aside className="sidebar">
      <div>
        <div className="sidebar-brand">
          <h1 className="sidebar-brand-title">Home Inventory</h1>
          <p className="sidebar-brand-subtitle">Warranty Tracker</p>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.label}
                to={item.to}
                className={({ isActive }) =>
                  `sidebar-link ${isActive ? "active" : ""}`
                }
              >
                <Icon size={18} strokeWidth={2} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      <button type="button" className="sidebar-logout" onClick={handleLogout}>
        <LogOut size={18} strokeWidth={2} />
        <span>Logout</span>
      </button>
    </aside>
  );
}
