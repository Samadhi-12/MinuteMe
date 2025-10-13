import { useState } from "react";
import api from "../lib/axios";
import "../App.css"; // We'll add styles here

function AnalyzeMeetingModal({ isOpen, onClose }) {
    const [videoUrl, setVideoUrl] = useState("");
    const [step, setStep] = useState("initial"); // 'initial', 'transcribing', 'transcribed', 'processing', 'done'
    const [message, setMessage] = useState("");

    const handleTranscribe = async () => {
        if (!videoUrl) {
            setMessage("Please enter a valid Google Drive URL.");
            return;
        }
        setStep("transcribing");
        setMessage("Transcribing video... This may take several minutes.");
        try {
            await api.post("/transcribe", { video_url: videoUrl });
            setStep("transcribed");
            setMessage("✅ Transcription successful! Ready to generate minutes.");
        } catch (error) {
            console.error("Transcription failed:", error);
            setStep("initial");
            setMessage(`❌ Transcription failed: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleProcessMeeting = async () => {
        setStep("processing");
        setMessage("Generating minutes and action items...");
        try {
            await api.post("/process-meeting");
            setStep("done");
            setMessage("🎉 Meeting processed successfully! You can view the results on the relevant pages.");
        } catch (error) {
            console.error("Processing failed:", error);
            setStep("transcribed"); // Go back to previous step on failure
            setMessage(`❌ Processing failed: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleClose = () => {
        // Reset state on close
        setVideoUrl("");
        setStep("initial");
        setMessage("");
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>Analyze a New Meeting</h2>
                <p className="modal-message">{message}</p>

                {step === "initial" && (
                    <div className="form-group">
                        <label htmlFor="videoUrl">Google Drive Video Link</label>
                        <input
                            id="videoUrl"
                            type="url"
                            value={videoUrl}
                            onChange={(e) => setVideoUrl(e.target.value)}
                            placeholder="https://drive.google.com/file/d/..."
                        />
                        <button onClick={handleTranscribe} className="form-submit-btn">
                            Transcribe
                        </button>
                    </div>
                )}

                {step === "transcribing" && <div className="loader"></div>}

                {step === "transcribed" && (
                    <button onClick={handleProcessMeeting} className="form-submit-btn">
                        Generate Minutes & Action Items
                    </button>
                )}

                {step === "processing" && <div className="loader"></div>}

                {step === "done" && (
                    <button onClick={handleClose} className="form-submit-btn">
                        Finish
                    </button>
                )}

                <button onClick={handleClose} className="modal-close-btn">
                    Close
                </button>
            </div>
        </div>
    );
}

export default AnalyzeMeetingModal;