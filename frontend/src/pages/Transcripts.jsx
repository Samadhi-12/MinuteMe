import { useState, useEffect } from "react";
import api from "../lib/axios";
import { formatDistanceToNow } from "date-fns";

function Transcripts() {
    const [transcripts, setTranscripts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");

    useEffect(() => {
        async function fetchTranscripts() {
            try {
                setLoading(true);
                const response = await api.get("/transcripts");
                setTranscripts(response.data);
            } catch (error) {
                setMessage("Failed to load transcripts.");
            } finally {
                setLoading(false);
            }
        }
        fetchTranscripts();
    }, []);

    const handleGenerateMinutes = async (transcriptId) => {
        setMessage("Generating minutes...");
        try {
            await api.post("/generate-minutes", { transcript_id: transcriptId });
            setMessage("Minutes generated successfully!");
        } catch (error) {
            setMessage("Error generating minutes.");
        }
    };

    if (loading) return (
        <div className="form-container">
            <h2>Transcripts</h2>
            <div className="loading-container">
                <div className="loader"></div>
                <p>Loading transcripts...</p>
            </div>
        </div>
    );

    const formatTranscriptPreview = (text) => {
        if (!text) return "No transcript content";
        return text.length > 150 ? `${text.substring(0, 150)}...` : text;
    };

    return (
        <div className="form-container">
            <div className="page-header">
                <h2>Meeting Transcripts</h2>
                <p className="subtitle">View and process your meeting recordings</p>
            </div>
            
            {message && <div className="message-banner">{message}</div>}
            
            {transcripts.length > 0 ? (
                <div className="grid-container">
                    {transcripts.map((transcript) => {
                        const createdAt = new Date(transcript.created_at);
                        
                        return (
                            <div key={transcript._id} className="card transcript-card">
                                <div className="card-header">
                                    <div className="date-time">
                                        <div className="date">{createdAt.toLocaleDateString()}</div>
                                        <div className="time">{createdAt.toLocaleTimeString()}</div>
                                    </div>
                                    <span className="time-ago">
                                        {formatDistanceToNow(createdAt, { addSuffix: true })}
                                    </span>
                                </div>
                                
                                <div className="transcript-preview">
                                    {formatTranscriptPreview(transcript.transcript)}
                                </div>
                                
                                <div className="card-actions">
                                    <button 
                                        onClick={() => handleGenerateMinutes(transcript._id)} 
                                        className="form-submit-btn"
                                    >
                                        Generate Minutes
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            ) : (
                <div className="empty-state">
                    <div className="empty-icon">📝</div>
                    <h3>No transcripts yet</h3>
                    <p>Upload a meeting recording from the dashboard to get started</p>
                </div>
            )}
        </div>
    );
}

export default Transcripts;