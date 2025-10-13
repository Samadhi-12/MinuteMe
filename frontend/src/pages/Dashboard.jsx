import React, { useState, useEffect } from "react";
import { getAgenda, postTranscript } from "../api";
import "./Dashboard.css";

// Mock data - in a real app, this would come from your API
const recentMeetings = [
	{
		id: 1,
		name: "Q4 Marketing Strategy",
		date: "2025-10-12",
		summary: "Discussed budget and social media campaigns...",
	},
	{
		id: 2,
		name: "Project Phoenix Kick-off",
		date: "2025-10-10",
		summary: "Defined initial scope and assigned roles...",
	},
	{
		id: 3,
		name: "Weekly Team Sync",
		date: "2025-10-08",
		summary: "Reviewed progress on current sprint tasks...",
	},
];

const upcomingActions = [
	{
		id: 1,
		task: "Finalize Q4 budget report",
		due: "2025-10-15",
		owner: "John Doe",
	},
	{
		id: 2,
		task: "Draft initial design mockups",
		due: "2025-10-17",
		owner: "Jane Smith",
	},
];

function Dashboard() {
	const [agenda, setAgenda] = useState(null);
	const [transcript, setTranscript] = useState("");
	const [minutes, setMinutes] = useState(null);
	const [actionItems, setActionItems] = useState([]);

	useEffect(() => {
		async function fetchAgenda() {
			const data = await getAgenda();
			setAgenda(data);
		}
		fetchAgenda();
	}, []);

	const handleGenerateMinutes = async () => {
		if (!transcript) return;
		const data = await postTranscript(transcript);
		setMinutes(data.minutes);
		setActionItems(data.action_items);
	};

	return (
		<div className="dashboard-container">
			<header className="dashboard-header">
				<h1>Welcome Back!</h1>
				<p>Ready to get your meetings organized?</p>
				<button className="primary-action-btn">+ Analyze New Meeting</button>
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
									View Details
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

			<section>
				<h2>Agenda</h2>
				{agenda ? (
					<ul>
						{agenda.agenda.map((item, idx) => (
							<li key={idx}>
								{item.topic} - {item.priority} ({item.time_allocated})
							</li>
						))}
					</ul>
				) : (
					<p>Loading agenda...</p>
				)}
			</section>

			<section>
				<h2>Enter Transcript</h2>
				<textarea
					value={transcript}
					onChange={(e) => setTranscript(e.target.value)}
					rows={6}
					cols={60}
				/>
				<br />
				<button onClick={handleGenerateMinutes}>
					Generate Minutes & Action Items
				</button>
			</section>

			{minutes && (
				<section>
					<h2>Minutes</h2>
					<pre>{JSON.stringify(minutes, null, 2)}</pre>
				</section>
			)}

			{actionItems.length > 0 && (
				<section>
					<h2>Action Items</h2>
					<ul>
						{actionItems.map((item, idx) => (
							<li key={idx}>
								{item.task} - {item.owner} - {item.deadline}
							</li>
						))}
					</ul>
				</section>
			)}
		</div>
	);
}

export default Dashboard;
