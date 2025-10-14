import { Link, useLocation } from "react-router-dom";
import { UserButton, useAuth, useUser } from "@clerk/clerk-react";
import { useUserRole } from "../hooks/useUserRole";
import "../App.css";
import { useEffect } from "react";

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
  const { isAdmin, isLoading } = useUserRole();
  const { session, isLoaded: isSessionLoaded } = useAuth();
  const { user, isLoaded: isUserLoaded } = useUser();

  // Enhanced debugging
  useEffect(() => {
    if (isSessionLoaded && isUserLoaded) {
      console.log("--- CLERK DEBUG (NAVBAR) ---");
      console.log("Session loaded:", isSessionLoaded);
      console.log("Session object:", session);
      console.log("User loaded:", isUserLoaded);
      console.log("User object:", user);
      
      if (user) {
        console.log("User public metadata:", user.publicMetadata);
        console.log("Is Admin:", isAdmin);
      }
      console.log("--------------------------");
    }
  }, [isSessionLoaded, session, isUserLoaded, user, isAdmin]);

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
          {/* Show admin link if user is admin and not still loading */}
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
      <UserButton afterSignOutUrl="/sign-in" />
    </nav>
  );
}

export default Navbar;
