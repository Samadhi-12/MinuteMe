import { useState } from "react";
import api from "../lib/axios";
import AnalyzeMeetingModal from "../components/AnalyzeMeetingModal"; // Import the modal

// Mock data for a more attractive UI
const recentMeetings = [
	{
		id: 1,
		name: "Q4 Marketing Strategy",
		date: "2025-10-12",
		summary:
			"Finalized budget allocations for social media campaigns and influencer collaborations.",
	},
	{
		id: 2,
		name: "Project Phoenix Kick-off",
		date: "2025-10-10",
		summary:
			"Defined the initial project scope, set key milestones, and assigned team roles.",
	},
];

const upcomingActions = [
	{ id: 1, task: "Finalize Q4 budget report", due: "2025-10-15", owner: "You" },
	{
		id: 2,
		task: "Draft initial design mockups for Project Phoenix",
		due: "2025-10-17",
		owner: "Jane S.",
	},
	{ id: 3, task: "Schedule follow-up with the design team", due: "2025-10-18", owner: "You" },
];

function Dashboard() {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleAnalyzeMeeting = () => {
        setIsModalOpen(true);
    };

    return (
        <div className="dashboard-container">
            <AnalyzeMeetingModal 
                isOpen={isModalOpen} 
                onClose={() => setIsModalOpen(false)} 
            />

            <header className="dashboard-header">
                <h1>Welcome Back!</h1>
                <p>Ready to turn your meetings into actionable outcomes?</p>
                <button
                    onClick={handleAnalyzeMeeting}
                    className="primary-action-btn"
                >
                    ✨ Analyze New Meeting
                </button>
            </header>

            <div className="dashboard-main-content">
                <section className="recent-meetings">
                    <h2>Recent Meetings</h2>
                    <div className="card-list">
                        {recentMeetings.map((meeting) => (
                            <div key={meeting.id} className="card meeting-card">
                                <h3>{meeting.name}</h3>
                                <p className="card-date">{meeting.date}</p>
                                <p className="card-summary">{meeting.summary}</p>
                                <a href="#" className="card-link">
                                    View Details →
                                </a>
                            </div>
                        ))}
                    </div>
                </section>

                <aside className="upcoming-actions">
                    <h2>Upcoming Action Items</h2>
                    <div className="action-item-list">
                        {upcomingActions.map((action) => (
                            <div key={action.id} className="card action-item-card">
                                <p className="action-task">{action.task}</p>
                                <p className="action-due">
                                    <strong>Due:</strong> {action.due} |{" "}
                                    <strong>Owner:</strong> {action.owner}
                                </p>
                            </div>
                        ))}
                    </div>
                </aside>
            </div>
        </div>
    );
}

export default Dashboard;
