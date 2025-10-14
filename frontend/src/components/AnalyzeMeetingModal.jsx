import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../lib/axios";
import { useUserRole } from "../hooks/useUserRole";
import { useAutomation } from "../context/AutomationContext"; // Import automation context
import "../App.css";

function AnalyzeMeetingModal({ isOpen, onClose, autoMode }) { // Receive autoMode prop
    const [videoUrl, setVideoUrl] = useState("");
    const [manualTranscript, setManualTranscript] = useState("");
    const [step, setStep] = useState("initial");
    const [message, setMessage] = useState("");
    const [transcriptionQuota, setTranscriptionQuota] = useState(5);
    const [quotaLoading, setQuotaLoading] = useState(true);
    const [newMinutesId, setNewMinutesId] = useState(null);
    const navigate = useNavigate();
    const { isPremium } = useUserRole();
    const { startAutomation } = useAutomation(); // Get startAutomation function
    
    // Fetch transcription quota on component mount
    useEffect(() => {
        if (!isPremium && isOpen) {
            fetchTranscriptionQuota();
        } else if (isPremium) {
            setQuotaLoading(false);
        }
    }, [isPremium, isOpen]);
    
    const fetchTranscriptionQuota = async () => {
        try {
            setQuotaLoading(true);
            // This would be a new endpoint to check remaining transcription quota
            const res = await api.get("/user/transcription-quota");
            setTranscriptionQuota(res.data.remaining);
        } catch (error) {
            console.error("Failed to fetch transcription quota:", error);
            setTranscriptionQuota(0); // Default to 0 if error
        } finally {
            setQuotaLoading(false);
        }
    };

    const handleUniversalSubmit = async (isManual = false) => {
        const meetingDate = new Date().toISOString().slice(0, 10);
        const meetingName = isManual 
            ? `Meeting from Transcript ${new Date().toLocaleTimeString()}`
            : `Meeting from Video ${new Date().toLocaleTimeString()}`;

        try {
            // Step 1: Create a meeting record first
            const meetingRes = await api.post("/meetings", {
                meeting_name: meetingName,
                meeting_date: meetingDate,
                status: "conducted",
            });
            const meetingId = meetingRes.data._id;

            if (autoMode) {
                // --- AUTOMATED FLOW ---
                const payload = { meeting_id: meetingId };
                if (isManual) {
                    payload.transcript_text = manualTranscript;
                } else {
                    payload.video_url = videoUrl;
                }
                await api.post("/process-automated", payload);
                startAutomation(meetingId, "🚀 Automation process started...");
                handleClose(); // Close the modal immediately
            } else {
                // --- MANUAL FLOW ---
                if (isManual) {
                    await handleManualSubmit(meetingId, meetingName, meetingDate);
                } else {
                    await handleTranscribe(meetingId, meetingName, meetingDate);
                }
            }
        } catch (error) {
            console.error("Processing failed:", error);
            setStep("initial");
            setMessage(`❌ Processing failed: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleTranscribe = async (meetingId, meetingName, meetingDate) => {
        // ... (this is now part of the manual flow)
        setStep("transcribing");
        setMessage("Transcribing video...");
        await api.post("/transcribe", { video_url: videoUrl, meeting_id: meetingId, meeting_name: meetingName, meeting_date: meetingDate });
        if (!isPremium) setTranscriptionQuota(prev => Math.max(0, prev - 1));
        setStep("transcribed");
        setMessage("✅ Transcription successful! Ready to generate minutes.");
    };
    
    const handleManualSubmit = async (meetingId, meetingName, meetingDate) => {
        // ... (this is now part of the manual flow)
        setStep("processing");
        setMessage("Saving transcript...");
        await api.post("/save-manual-transcript", { transcript: manualTranscript, meeting_id: meetingId, meeting_name: meetingName, meeting_date: meetingDate });
        setStep("transcribed");
        setMessage("✅ Transcript saved! Ready to generate minutes.");
    };

    const handleGenerateMinutes = async () => {
        setStep("processing");
        setMessage("Generating minutes...");
        try {
            // This endpoint should be smart enough to find the latest transcript
            const response = await api.post("/generate-minutes");
            setNewMinutesId(response.data._id); // <-- Capture the new minutes ID
            setStep("done");
            setMessage("🎉 Minutes generated successfully! Let's review them.");
        } catch (error) {
            console.error("Processing failed:", error);
            setStep("transcribed");
            setMessage(`❌ Minutes generation failed: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleFinishAndNavigate = () => {
        handleClose();
        navigate(`/minutes/${newMinutesId}`); // <-- Navigate to the specific minute detail page
    };

    const handleClose = () => {
        // Reset state on close
        setVideoUrl("");
        setManualTranscript("");
        setStep("initial");
        setMessage("");
        setNewMinutesId(null); // <-- Reset the ID on close
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button onClick={handleClose} className="modal-close-btn" aria-label="Close modal">&times;</button>
                <h2>Analyze a New Meeting</h2>
                {message && <p className="modal-message">{message}</p>}

                {step === "initial" && (
                    <div className="meeting-input-options">
                        {/* Video Transcription Form */}
                        <div className="input-option">
                            <h3>Option 1: From Video</h3>
                            {!isPremium && !quotaLoading && (
                                <div className="quota-display">
                                    <span className={transcriptionQuota > 0 ? "quota-available" : "quota-depleted"}>
                                        {transcriptionQuota} video transcriptions left
                                    </span>
                                </div>
                            )}
                            {(!isPremium && transcriptionQuota === 0) && (
                                <div className="upgrade-prompt" style={{padding: '0.5rem', margin: '0 0 1rem 0'}}>
                                    <span>Quota reached. </span>
                                    <Link to="/upgrade" className="upgrade-link">Upgrade to Premium</Link>
                                </div>
                            )}
                            <div className="form-group">
                                <label htmlFor="videoUrl">Google Drive Video Link</label>
                                <input
                                    id="videoUrl"
                                    type="url"
                                    value={videoUrl}
                                    onChange={(e) => setVideoUrl(e.target.value)}
                                    placeholder="https://drive.google.com/file/d/..."
                                    disabled={!isPremium && transcriptionQuota <= 0}
                                />
                                <button 
                                    onClick={() => handleUniversalSubmit(false)} 
                                    className="form-submit-btn"
                                    disabled={!isPremium && transcriptionQuota <= 0}
                                >
                                    {autoMode ? "🚀 Start Automation" : "Transcribe Video"}
                                </button>
                            </div>
                        </div>
                        
                        <div className="option-divider"><span>OR</span></div>
                        
                        {/* Manual Transcript Form */}
                        <div className="input-option">
                            <h3>Option 2: From Text</h3>
                            <div className="form-group">
                                <label htmlFor="manualTranscript">Paste Meeting Transcript</label>
                                <textarea
                                    id="manualTranscript"
                                    value={manualTranscript}
                                    onChange={(e) => setManualTranscript(e.target.value)}
                                    placeholder="Paste or type meeting transcript here..."
                                    rows="8"
                                />
                                <button onClick={() => handleUniversalSubmit(true)} className="form-submit-btn">
                                    {autoMode ? "🚀 Start Automation" : "Process Transcript"}
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {step === "transcribing" && (
                    <div className="processing-state">
                        <div className="loader"></div>
                        <p>Transcribing your meeting video...</p>
                        <p className="processing-note">This may take several minutes.</p>
                    </div>
                )}

                {step === "transcribed" && (
                    <div className="success-state">
                        <div className="success-icon">📄</div>
                        <h3>Transcription Ready</h3>
                        <p>Your meeting text is ready. Let's generate the minutes.</p>
                        <button onClick={handleGenerateMinutes} className="form-submit-btn">
                            Generate Minutes
                        </button>
                    </div>
                )}

                {step === "processing" && (
                    <div className="processing-state">
                        <div className="loader"></div>
                        <p>Generating minutes and action items...</p>
                        <p className="processing-note">This is where the magic happens.</p>
                    </div>
                )}

                {step === "done" && (
                    <div className="success-state">
                        <div className="success-icon">🎉</div>
                        <h3>All Done!</h3>
                        <p>Your meeting has been fully processed.</p>
                        <button onClick={handleFinishAndNavigate} className="form-submit-btn">
                            Review Minutes & Actions
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AnalyzeMeetingModal;