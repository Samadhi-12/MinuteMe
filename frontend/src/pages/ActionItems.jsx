import { useState, useEffect } from "react";
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
			const response = await fetch("http://localhost:8000/action-items");
			const data = await response.json();

			if (data && data.action_items) {
				const formattedItems = data.action_items.map((item, index) => ({
					id: index + 1,
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
		try {
			await fetch(`http://localhost:8000/action-items/${id}/status`, {
				method: "PATCH",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ status: newStatus }),
			});

			setActionItems(items =>
				items.map(item =>
					item.id === id ? { ...item, status: newStatus } : item
				)
			);
		} catch (error) {
			console.error("Error updating status:", error);
		}
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
