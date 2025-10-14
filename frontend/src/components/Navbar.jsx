import { Link, useLocation } from "react-router-dom";
import { UserButton, useAuth } from "@clerk/clerk-react";
import { useUserRole } from "../hooks/useUserRole";
import "../App.css";

const navLinks = [
  { to: "/", label: "Dashboard" },
  { to: "/agenda", label: "My Agendas" },
  { to: "/meetings", label: "Meetings" }, 
  { to: "/transcripts", label: "Transcripts" },
  { to: "/minutes", label: "My Minutes" },
  { to: "/action-items", label: "Action Items" },  
  { to: "/calendar", label: "Calendar" },
];

function Navbar() {
    const location = useLocation();
    const { isAdmin, isPremium, tier, isLoading } = useUserRole();
    
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
                    {!isLoading && isAdmin && (
                        <li>
                            <Link
                                to="/admin"
                                className={location.pathname === '/admin' ? 'active' : ''}
                            >
                                Admin
                            </Link>
                        </li>
                    )}
                </ul>
            </div>
            
            <div className="user-controls">
                <span className={`tier-badge tier-${tier}`}>
                    {tier === "premium" ? "Premium" : "Free"}
                </span>
                {!isPremium && (
                    <Link to="/upgrade" className="upgrade-button">
                        Upgrade
                    </Link>
                )}
                <UserButton afterSignOutUrl="/sign-in" />
            </div>
        </nav>
    );
}

export default Navbar;
