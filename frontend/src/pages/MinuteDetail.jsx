import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../lib/axios";

function MinuteDetail() {
    const { id } = useParams();
    const [minute, setMinute] = useState(null);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchMinute = async () => {
            try {
                setLoading(true);
                const response = await api.get(`/minutes/${id}`);
                setMinute(response.data);
            } catch (error) {
                console.error("Failed to fetch minute details", error);
                setMessage("Could not load minute details.");
            } finally {
                setLoading(false);
            }
        };
        fetchMinute();
    }, [id]);

    const handleGenerateActions = async () => {
        setMessage("Generating action items... This may take a moment.");
        try {
            await api.post("/generate-action-items", { minutes_id: id });
            setMessage("✅ Action items generated and scheduled successfully! Refreshing...");
            // Refresh data after a short delay
            setTimeout(() => window.location.reload(), 2000);
        } catch (error) {
            console.error("Failed to generate action items", error);
            setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`);
        }
    };

    if (loading) return <p>Loading details...</p>;
    if (!minute) return <p>Minute not found.</p>;

    return (
        <div className="form-container">
            <h2>Meeting of {minute.date}</h2>
            {message && <p>{message}</p>}
            
            <div className="detail-section">
                <h3>Summary</h3>
                <p>{minute.summary}</p>
            </div>

            <div className="detail-section">
                <h3>Key Decisions</h3>
                {minute.decisions?.length > 0 ? (
                    <ul>{minute.decisions.map((d, i) => <li key={i}>{d}</li>)}</ul>
                ) : <p>No key decisions were recorded.</p>}
            </div>

            <div className="detail-section">
                <h3>Topics for Future Discussion</h3>
                {minute.future_discussion_points?.length > 0 ? (
                    <ul>{minute.future_discussion_points.map((t, i) => <li key={i}>{t}</li>)}</ul>
                ) : <p>No future topics were recorded.</p>}
            </div>

            <div className="detail-section">
                <h3>Action Items</h3>
                {minute.action_items?.length > 0 ? (
                    <ul>{minute.action_items.map((item, i) => <li key={i}><strong>{item.owner}:</strong> {item.task}</li>)}</ul>
                ) : (
                    <>
                        <p>No action items have been generated for this meeting yet.</p>
                        <button onClick={handleGenerateActions} className="form-submit-btn" style={{marginTop: '1em'}}>
                            Generate & Schedule Action Items
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}

export default MinuteDetail;