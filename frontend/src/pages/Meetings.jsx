import { useState, useEffect } from "react";
import api from "../lib/axios";

function Meetings() {
    const [meetings, setMeetings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");
    const [selectedMeeting, setSelectedMeeting] = useState(null);
    const [showTranscribeModal, setShowTranscribeModal] = useState(false);
    const [driveLink, setDriveLink] = useState("");
    const [meetingDate, setMeetingDate] = useState("");
    const [meetingName, setMeetingName] = useState("");

    useEffect(() => {
        async function fetchMeetings() {
            try {
                setLoading(true);
                const response = await api.get("/meetings");
                setMeetings(response.data);
            } catch (error) {
                setMessage("Failed to load meetings.");
            } finally {
                setLoading(false);
            }
        }
        fetchMeetings();
    }, []);

    const handleStatusChange = async (meeting, status) => {
        console.log(`[DEBUG] Changing status for meeting ${meeting._id} to ${status}`);
        try {
            await api.patch(`/meetings/${meeting._id}`, { status });
            setMeetings(meetings.map(m => m._id === meeting._id ? { ...m, status } : m));
            console.log(`[DEBUG] Status updated for meeting ${meeting._id}`);
        } catch (error) {
            console.error("[DEBUG] Failed to update status:", error);
            setMessage("Failed to update status.");
        }
    };

    const handleShowTranscribe = (meeting) => {
        console.log(`[DEBUG] Opening transcribe modal for meeting ${meeting._id}`);
        setSelectedMeeting(meeting);
        setShowTranscribeModal(true);
        setDriveLink("");
        setMeetingDate(meeting.meeting_date || new Date().toISOString().slice(0, 10));
        setMeetingName(meeting.meeting_name || `Meeting ${meeting._id.slice(-4)}`);
    };

    const handleTranscribe = async () => {
        console.log(`[DEBUG] Submitting transcript for meeting ${selectedMeeting?._id} with link: ${driveLink}`);
        if (!driveLink) {
            setMessage("Please enter a valid Google Drive link.");
            return;
        }
        setMessage("Transcribing video... This may take several minutes.");
        try {
            const res = await api.post("/transcribe", {
                video_url: driveLink,
                meeting_date: meetingDate,
                meeting_name: meetingName,
                meeting_id: selectedMeeting._id
            });
            console.log("[DEBUG] Transcribe response:", res.data);
            setMessage("Transcription successful! Minutes will be generated next.");
            setShowTranscribeModal(false);
        } catch (error) {
            console.error("[DEBUG] Transcription failed:", error);
            setMessage("Transcription failed.");
        }
    };

    const handleDelete = async (id) => {
        try {
            await api.delete(`/meetings/${id}`);
            setMeetings(meetings.filter(m => m._id !== id));
            setMessage("Meeting deleted.");
        } catch (error) {
            setMessage("Failed to delete meeting.");
        }
    };

    if (loading) return <p>Loading meetings...</p>;

    return (
        <div className="form-container">
            <h2>Upcoming Meetings</h2>
            {message && <p>{message}</p>}
            {meetings.length > 0 ? (
                <div className="card-list">
                    {meetings.map((meeting) => (
                        <div key={meeting._id} className="card">
                            <h3>{meeting.meeting_name}</h3>
                            <p>Date: {meeting.meeting_date}</p>
                            <p>Status: {meeting.status || "scheduled"}</p>
                            <p>Agenda: {meeting.agenda_id}</p>
                            <div style={{ marginTop: "1em" }}>
                                <button
                                    className="form-submit-btn"
                                    onClick={() => handleStatusChange(meeting, "conducted")}
                                    disabled={meeting.status === "conducted"}
                                >
                                    Mark as Conducted
                                </button>
                                <button
                                    className="form-submit-btn"
                                    style={{ marginLeft: "1em" }}
                                    onClick={() => handleStatusChange(meeting, "dismissed")}
                                    disabled={meeting.status === "dismissed"}
                                >
                                    Dismiss
                                </button>
                                {meeting.status === "conducted" && (
                                    <button
                                        className="form-submit-btn"
                                        style={{ marginLeft: "1em" }}
                                        onClick={() => handleShowTranscribe(meeting)}
                                    >
                                        Paste Drive Link
                                    </button>
                                )}
                                <button
                                    className="form-submit-btn danger"
                                    style={{ marginLeft: "1em" }}
                                    onClick={() => handleDelete(meeting._id)}
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No meetings scheduled.</p>
            )}

            {/* Transcribe Modal */}
            {showTranscribeModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Paste Drive Link for Meeting</h3>
                        <div className="form-group">
                            <label htmlFor="driveLink">Google Drive Link</label>
                            <input
                                id="driveLink"
                                type="url"
                                value={driveLink}
                                onChange={e => setDriveLink(e.target.value)}
                                placeholder="https://drive.google.com/file/d/..."
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="meetingDate">Meeting Date</label>
                            <input
                                id="meetingDate"
                                type="date"
                                value={meetingDate}
                                onChange={e => setMeetingDate(e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="meetingName">Meeting Name (optional)</label>
                            <input
                                id="meetingName"
                                type="text"
                                value={meetingName}
                                onChange={e => setMeetingName(e.target.value)}
                                placeholder="Meeting name"
                            />
                        </div>
                        <button className="form-submit-btn" onClick={handleTranscribe}>
                            Submit & Transcribe
                        </button>
                        <button className="modal-close-btn" onClick={() => setShowTranscribeModal(false)}>
                            Cancel
                        </button>
                        {message && <p>{message}</p>}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Meetings;