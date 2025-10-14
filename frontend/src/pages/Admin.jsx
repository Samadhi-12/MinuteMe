import { useEffect, useState } from "react";
import api from "../lib/axios";
import { useUserRole } from "../hooks/useUserRole";
import { useNavigate } from "react-router-dom";

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
        await api.patch(`/admin/user/${userId}/tier`, { tier: newTier });
        setUsers(users => users.map(u => u.id === userId ? { ...u, tier: newTier } : u));
        setMessage("Tier updated.");
    };

    const handleRoleChange = async (userId, newRole) => {
        if (!window.confirm(`Change role for user ${userId} to ${newRole}?`)) return;
        setMessage("Updating role...");
        await api.patch(`/admin/user/${userId}/role`, { role: newRole });
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
                <div className="loading-spinner"></div>
            </div>
        );
    }

    return (
        <div className="form-container">
            <h2>Admin Dashboard</h2>
            <h3>User Management</h3>
            {message && <div className="message-banner">{message}</div>}
            <input
                type="text"
                placeholder="Search users..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                style={{ marginBottom: "1em", padding: "0.5em", width: "100%" }}
            />
            <table>
                <thead>
                    <tr>
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
                            <td>{u.first_name} {u.last_name}</td>
                            <td>{u.email}</td>
                            <td>
                                <span className={`badge badge-${u.role}`}>{u.role}</span>
                                <button
                                    style={{ marginLeft: "0.5em" }}
                                    onClick={() => handleRoleChange(u.id, u.role === "admin" ? "user" : "admin")}
                                >
                                    Set {u.role === "admin" ? "User" : "Admin"}
                                </button>
                            </td>
                            <td>
                                <span className={`badge badge-${u.tier}`}>{u.tier}</span>
                                <button
                                    style={{ marginLeft: "0.5em" }}
                                    onClick={() => handleTierChange(u.id, u.tier === "premium" ? "free" : "premium")}
                                >
                                    Set {u.tier === "premium" ? "Free" : "Premium"}
                                </button>
                            </td>
                            <td>
                                <button
                                    className="danger"
                                    onClick={() => handleDeleteUser(u.id)}
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default AdminDashboard;