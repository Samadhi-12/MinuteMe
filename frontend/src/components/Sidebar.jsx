import { Link, useLocation } from "react-router-dom";
import { Settings, History, Crown } from "lucide-react";
import "../App.css";

const sidebarLinks = [
  { to: "/settings", label: "Settings", icon: <Settings size={20} /> },
  { to: "/history", label: "History", icon: <History size={20} /> },
  { to: "/upgrade", label: "Upgrade", icon: <Crown size={20} /> },
];

function Sidebar({ visible, onClose }) {
  const location = useLocation();
  return (
    <aside className={`sidebar${visible ? " sidebar-visible" : ""}`}>
      <button className="sidebar-close-btn" onClick={onClose} aria-label="Close sidebar">×</button>
      <ul className="sidebar-links">
        {sidebarLinks.map(link => (
          <li key={link.to} className={location.pathname === link.to ? "active" : ""}>
            <Link to={link.to} className="sidebar-link">
              {link.icon}
              <span className="sidebar-label">{link.label}</span>
            </Link>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;