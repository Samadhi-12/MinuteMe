import { useUserRole } from "../hooks/useUserRole";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function AdminDashboard() {
    const { isAdmin, isLoading } = useUserRole();
    const navigate = useNavigate();

    useEffect(() => {
        // Redirect non-admins once we confirm they're not admin
        if (!isLoading && !isAdmin) {
            navigate("/");
        }
    }, [isAdmin, isLoading, navigate]);

    if (isLoading) {
        return (
            <div className="form-container">
                <h2>Loading Admin Dashboard</h2>
                <div className="loading-spinner"></div>
            </div>
        );
    }

    // This is still needed for immediate protection
    if (!isAdmin) {
        return (
            <div className="form-container">
                <h2>Access Denied</h2>
                <p>You do not have permission to view this page.</p>
            </div>
        );
    }

    return (
        <div className="form-container">
            <h2>Admin Dashboard</h2>
            <p>Welcome, Admin! This is where you can manage users and site settings.</p>
            {/* Admin tools will go here */}
        </div>
    );
}

export default AdminDashboard;