import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../lib/axios";
import { formatDistanceToNow } from "date-fns";

function MinutesList() {
    const [minutes, setMinutes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchMinutes = async () => {
        try {
            setLoading(true);
            const response = await api.get("/minutes");
            // Sort by most recent first
            const sortedMinutes = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            setMinutes(sortedMinutes);
            setError(null);
        } catch (error) {
            console.error("Failed to fetch minutes", error);
            setError("Could not load your minutes. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMinutes();

        // Add event listener to refetch data when the window/tab gets focus
        window.addEventListener('focus', fetchMinutes);

        // Cleanup function to remove the event listener
        return () => {
            window.removeEventListener('focus', fetchMinutes);
        };
    }, []);

    if (loading) return (
        <div className="form-container">
            <div className="page-header">
                <h2>My Minutes</h2>
                <p className="subtitle">A record of all your processed meetings</p>
            </div>
            <div className="loading-container">
                <div className="loader"></div>
                <p>Loading minutes...</p>
            </div>
        </div>
    );

    if (error) return <div className="message-banner">{error}</div>;

    return (
        <div className="form-container">
            <div className="page-header">
                <h2>My Minutes</h2>
                <p className="subtitle">A record of all your processed meetings</p>
            </div>

            {minutes.length > 0 ? (
                <div className="grid-container">
                    {minutes.map((minute) => (
                        <div key={minute._id} className="card">
                            <div className="card-header">
                                <h3>{minute.meeting_name || `Meeting of ${minute.date}`}</h3>
                                <span className="time-ago">
                                    {formatDistanceToNow(new Date(minute.created_at), { addSuffix: true })}
                                </span>
                            </div>
                            <p className="card-summary">{minute.summary}</p>
                            <Link to={`/minutes/${minute._id}`} className="card-link">
                                View Details & Actions →
                            </Link>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="empty-state">
                    <div className="empty-icon">📝</div>
                    <h3>No minutes found</h3>
                    <p>Go to the Dashboard or Transcripts page to analyze a meeting.</p>
                </div>
            )}
        </div>
    );
}

export default MinutesList;
