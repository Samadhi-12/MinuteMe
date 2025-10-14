import { Link, useLocation } from "react-router-dom";
import { UserButton } from "@clerk/clerk-react";
import "../App.css";

const navLinks = [
  { to: "/", label: "Dashboard" },
  { to: "/create-agenda", label: "Create Agenda" },
  { to: "/agenda", label: "My Agendas" },
  { to: "/meetings", label: "Meetings" }, 
  { to: "/transcripts", label: "Transcripts" },
  { to: "/minutes", label: "My Minutes" },
  { to: "/calendar", label: "Calendar" },
  { to: "/action-items", label: "Action Items" },
];

function Navbar() {
  const location = useLocation();
  return (
    <nav>
      <div style={{ display: 'flex', alignItems: 'center', gap: '2em' }}>
        <Link to="/" style={{ textDecoration: 'none' }}>
          <div style={{ fontWeight: 700, fontSize: 20, color: "#fff", letterSpacing: 1 }}>
            MinuteMe
          </div>
        </Link>
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
      </div>
      <UserButton afterSignOutUrl="/sign-in" />
    </nav>
  );
}

export default Navbar;
