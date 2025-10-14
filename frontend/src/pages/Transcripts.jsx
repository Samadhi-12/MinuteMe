import { useState, useEffect } from "react";
import api from "../lib/axios";

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

    if (loading) return <p>Loading transcripts...</p>;

    return (
        <div className="form-container">
            <h2>Transcripts</h2>
            {message && <p>{message}</p>}
            {transcripts.length > 0 ? (
                <div className="card-list">
                    {transcripts.map((t) => (
                        <div key={t._id} className="card">
                            <p>{t.transcript.slice(0, 100)}...</p>
                            <button onClick={() => handleGenerateMinutes(t._id)} className="form-submit-btn">
                                Generate Minutes
                            </button>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No transcripts found.</p>
            )}
        </div>
    );
}

export default Transcripts;