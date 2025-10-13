import { useState, useEffect } from "react";
import api from "../lib/axios"; // Use the authenticated api instance
import "../App.css";

function ActionItems() {
    const [actionItems, setActionItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchActionItems();
    }, []);

    const fetchActionItems = async () => {
        try {
            setLoading(true);
            // Use the authenticated api instance and correct endpoint
            const response = await api.get("/action-items");
            const data = response.data;

            if (data) {
                const formattedItems = data.map((item, index) => ({
                    id: item._id || index + 1, // Prefer a real ID if available
                    task: item.task || item.action,
                    owner: item.owner || item.assignee,
                    deadline: item.deadline || item.due_date || "TBD",
                    status: item.status || "pending",
                }));
                setActionItems(formattedItems);
            }
        } catch (error) {
            console.error("Error fetching action items:", error);
            setError("Failed to load action items");
        } finally {
            setLoading(false);
        }
    };

    const handleStatusChange = async (id, newStatus) => {
        // This endpoint doesn't exist yet, so we'll just update the local state for now.
        // In a real app, you would implement a PATCH /action-items/{id} endpoint.
        setActionItems(items =>
            items.map(item =>
                item.id === id ? { ...item, status: newStatus } : item
            )
        );
    };

    const getStatusColor = (status) => {
        switch (status) {
            case "completed": return "#4ade80";
            case "in-progress": return "#fbbf24";
            case "pending": return "#ef4444";
            default: return "#a0aec0";
        }
    };

    if (loading) return <div className="action-items-container"><p>Loading action items...</p></div>;
    if (error) return <div className="action-items-container"><p className="error">{error}</p></div>;

    return (
        <div className="action-items-container">
            <h2>Action Items</h2>
            {actionItems.length > 0 ? (
                <div className="action-items-list">
                    {actionItems.map((item) => (
                        <div key={item.id} className="action-item-card">
                            <div className="action-item-header">
                                <h3>{item.task}</h3>
                                <span 
                                    className="status-indicator"
                                    style={{ backgroundColor: getStatusColor(item.status) }}
                                >
                                    {item.status}
                                </span>
                            </div>
                            <div className="action-item-details">
                                <p><strong>Owner:</strong> {item.owner}</p>
                                <p><strong>Deadline:</strong> {item.deadline}</p>
                            </div>
                            <div className="action-item-buttons">
                                <button 
                                    onClick={() => handleStatusChange(item.id, "in-progress")}
                                    className="status-button in-progress"
                                >
                                    Mark In Progress
                                </button>
                                <button 
                                    onClick={() => handleStatusChange(item.id, "completed")}
                                    className="status-button completed"
                                >
                                    Mark Complete
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p className="no-items">No action items available. Create minutes from Dashboard first.</p>
            )}
        </div>
    );
}

export default ActionItems;
