import {
  Bell,
  Box,
  LayoutDashboard,
  LogOut,
  Settings,
  User,
} from "lucide-react";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, href: "/" },
  { label: "Inventory", icon: Box, href: "/inventory" },
  { label: "Notifications", icon: Bell, href: "/notifications" },
  { label: "Profile", icon: User, href: "/profile" },
  { label: "Settings", icon: Settings, href: "/settings" },
];

export default function Sidebar() {
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
              <a
                key={item.label}
                href={item.href}
                className={`sidebar-link ${item.href === "/" ? "active" : ""}`}
              >
                <Icon size={18} strokeWidth={2} />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>
      </div>

      <button type="button" className="sidebar-logout">
        <LogOut size={18} strokeWidth={2} />
        <span>Logout</span>
      </button>
    </aside>
  );
}