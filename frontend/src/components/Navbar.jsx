import { Link, useLocation } from "react-router-dom";
import "../App.css";

const navLinks = [
  { to: "/", label: "Dashboard" },
  { to: "/create-agenda", label: "Create Agenda" },
  { to: "/agenda", label: "Agenda" },
  { to: "/minutes", label: "Minutes" },
  { to: "/action-items", label: "Action Items" },
  { to: "/history", label: "History" },
  { to: "/settings", label: "Settings" },
];

function Navbar() {
  const location = useLocation();
  return (
    <header>
      <nav>
        <div style={{ fontWeight: 700, fontSize: 24, color: "#fff", letterSpacing: 1 }}>
          MinuteMe
        </div>
        <ul>
          {navLinks.map((link) => (
            <li key={link.to}>
              <Link
                to={link.to}
                className={location.pathname === link.to ? 'active' : ''}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}

export default Navbar;
