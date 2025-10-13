import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../lib/axios";

function MinutesList() {
	const [minutes, setMinutes] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		async function fetchMinutes() {
			try {
				setLoading(true);
				// This endpoint doesn't exist yet, so we'll create it.
				const response = await api.get("/minutes");
				setMinutes(response.data);
			} catch (error) {
				console.error("Failed to fetch minutes", error);
			} finally {
				setLoading(false);
			}
		}
		fetchMinutes();
	}, []);

	if (loading) return <p>Loading minutes...</p>;

	return (
		<div className="form-container">
			<h2>My Minutes</h2>
			{minutes.length > 0 ? (
				<div className="card-list">
					{minutes.map((minute) => (
						<div key={minute._id} className="card">
							<h3>Meeting of {minute.date}</h3>
							<p className="card-summary">{minute.summary}</p>
							<Link to={`/minutes/${minute._id}`} className="card-link">
								View Details & Actions →
							</Link>
						</div>
					))}
				</div>
			) : (
				<p>No minutes found. Go to the Dashboard to analyze a meeting.</p>
			)}
		</div>
	);
}

export default MinutesList;
