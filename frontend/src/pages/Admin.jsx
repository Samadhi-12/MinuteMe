import { useEffect, useState } from "react";
import api from "../lib/axios";
import { useUserRole } from "../hooks/useUserRole";
import { useNavigate } from "react-router-dom";
import { Crown, Users, ShieldCheck, UserMinus } from "lucide-react";
import "../components/UI.css";

function AdminDashboard() {
    const { isAdmin, isLoading } = useUserRole();
    const navigate = useNavigate();
    const [users, setUsers] = useState([]);
    const [loadingUsers, setLoadingUsers] = useState(true);
    const [search, setSearch] = useState("");
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (!isLoading && !isAdmin) navigate("/");
        if (isAdmin) {
            api.get("/admin/users")
                .then(res => {
                    setUsers(res.data);
                    setLoadingUsers(false);
                })
                .catch(err => {
                    setLoadingUsers(false);
                    if (err.response?.status === 403) navigate("/");
                });
        }
    }, [isAdmin, isLoading, navigate]);

    const handleTierChange = async (userId, newTier) => {
        if (!window.confirm(`Change tier for user ${userId} to ${newTier}?`)) return;
        setMessage("Updating tier...");
        // --- FIX: Send 'newTier' as a query parameter, not a request body ---
        await api.patch(`/admin/user/${userId}/tier?tier=${newTier}`);
        setUsers(users => users.map(u => u.id === userId ? { ...u, tier: newTier } : u));
        setMessage("Tier updated.");
    };

    const handleRoleChange = async (userId, newRole) => {
        if (!window.confirm(`Change role for user ${userId} to ${newRole}?`)) return;
        setMessage("Updating role...");
        // --- FIX: Send 'newRole' as a query parameter for consistency ---
        await api.patch(`/admin/user/${userId}/role?role=${newRole}`);
        setUsers(users => users.map(u => u.id === userId ? { ...u, role: newRole } : u));
        setMessage("Role updated.");
    };

    const handleDeleteUser = async (userId) => {
        if (!window.confirm(`Delete user ${userId}? This cannot be undone.`)) return;
        setMessage("Deleting user...");
        await api.delete(`/admin/user/${userId}`);
        setUsers(users => users.filter(u => u.id !== userId));
        setMessage("User deleted.");
    };

    const filteredUsers = users.filter(u =>
        u.email.toLowerCase().includes(search.toLowerCase()) ||
        `${u.first_name} ${u.last_name}`.toLowerCase().includes(search.toLowerCase())
    );

    if (isLoading || loadingUsers) {
        return (
            <div className="form-container">
                <h2>Loading Admin Dashboard</h2>
                <div className="loading-container">
                    <div className="loader"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="form-container admin-dashboard">
            <div className="page-header" style={{ textAlign: "center" }}>
                <h2>
                    <ShieldCheck size={28} style={{ color: "#3b82f6", verticalAlign: "middle" }} /> Admin Dashboard
                </h2>
                <p className="subtitle">Manage users, roles, and tiers</p>
            </div>
            {message && <div className="message-banner">{message}</div>}
            <div className="admin-controls">
                <input
                    type="text"
                    placeholder="Search users..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="admin-search"
                />
            </div>
            <div className="admin-table-container">
                <table className="admin-table">
                    <thead>
                        <tr>
                            <th><Users size={18} /></th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Tier</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredUsers.map(u => (
                            <tr key={u.id}>
                                <td>
                                    {u.role === "admin" ? (
                                        <ShieldCheck size={20} style={{ color: "#3b82f6" }} />
                                    ) : (
                                        <Users size={20} style={{ color: "#6b7280" }} />
                                    )}
                                </td>
                                <td>{u.first_name} {u.last_name}</td>
                                <td>{u.email}</td>
                                <td>
                                    <span className={`badge badge-role badge-${u.role}`}>
                                        {u.role === "admin" ? <ShieldCheck size={14} /> : <Users size={14} />}
                                        {u.role.charAt(0).toUpperCase() + u.role.slice(1)}
                                    </span>
                                    <button
                                        className="admin-action-btn"
                                        onClick={() => handleRoleChange(u.id, u.role === "admin" ? "user" : "admin")}
                                    >
                                        Set {u.role === "admin" ? "User" : "Admin"}
                                    </button>
                                </td>
                                <td>
                                    <span className={`badge badge-tier badge-${u.tier}`}>
                                        {u.tier === "premium" ? <Crown size={14} /> : null}
                                        {u.tier.charAt(0).toUpperCase() + u.tier.slice(1)}
                                    </span>
                                    <button
                                        className="admin-action-btn"
                                        onClick={() => handleTierChange(u.id, u.tier === "premium" ? "free" : "premium")}
                                    >
                                        Set {u.tier === "premium" ? "Free" : "Premium"}
                                    </button>
                                </td>
                                <td>
                                    <button
                                        className="danger admin-action-btn"
                                        onClick={() => handleDeleteUser(u.id)}
                                    >
                                        <UserMinus size={16} /> Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AdminDashboard;