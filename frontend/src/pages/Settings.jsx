import { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom"; // Import Link
import api from "../lib/axios";
import { useUserRole } from "../hooks/useUserRole"; // Import the user role hook

function Settings() {
    const [isConnected, setIsConnected] = useState(false);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");
    const location = useLocation();
    const { isPremium } = useUserRole(); // Get the user's premium status

    // Check connection status on load
    useEffect(() => {
        const checkStatus = async () => {
            try {
                setLoading(true);
                const res = await api.get("/auth/google/status");
                setIsConnected(res.data.is_connected);
            } catch (error) {
                setMessage("Could not check calendar connection status.");
            } finally {
                setLoading(false);
            }
        };
        checkStatus();
    }, []);

    // Handle the redirect back from Google
    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const code = params.get("code");

        if (code) {
            setMessage("Connecting to Google Calendar...");
            api.post("/auth/google/exchange", { code })
                .then(() => {
                    setIsConnected(true);
                    setMessage("✅ Successfully connected to Google Calendar!");
                    // Clean the URL
                    window.history.replaceState({}, document.title, "/settings");
                })
                .catch(() => {
                    setMessage("❌ Failed to connect to Google Calendar.");
                });
        }
    }, [location]);

    const handleConnect = async () => {
        try {
            const res = await api.get("/auth/google/url");
            window.location.href = res.data.authorization_url;
        } catch (error) {
            setMessage("Could not initiate connection. Please try again.");
        }
    };

    const handleDisconnect = async () => {
        if (window.confirm("Are you sure you want to disconnect your Google Calendar?")) {
            try {
                await api.post("/auth/google/disconnect");
                setIsConnected(false);
                setMessage("Google Calendar has been disconnected.");
            } catch (error) {
                setMessage("Failed to disconnect. Please try again.");
            }
        }
    };

    return (
        <div className="form-container">
            <div className="page-header">
                <h2>Settings</h2>
                <p className="subtitle">Manage your application settings and integrations.</p>
            </div>

            {message && <div className="message-banner">{message}</div>}

            <div className="card">
                <h3>Integrations</h3>
                <div className="integration-item">
                    <h4>Google Calendar</h4>
                    <p>Connect your Google Calendar to automatically schedule action items.</p>
                    
                    {/* --- MODIFIED: Conditional UI based on premium status --- */}
                    {!isPremium ? (
                        <div className="upgrade-prompt" style={{textAlign: 'left', padding: '1rem'}}>
                            <span>This is a Premium feature.</span>
                            <Link to="/upgrade" className="upgrade-link">Upgrade to connect</Link>
                        </div>
                    ) : loading ? (
                        <div className="loader"></div>
                    ) : isConnected ? (
                        <button className="danger" onClick={handleDisconnect}>
                            Disconnect Calendar
                        </button>
                    ) : (
                        <button className="primary-action-btn" onClick={handleConnect}>
                            Connect Google Calendar
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Settings;
