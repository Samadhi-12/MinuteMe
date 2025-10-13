import { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import api from "../lib/axios";
import "../App.css";

function AnalyzeMeetingModal({ isOpen, onClose }) {
    const [videoUrl, setVideoUrl] = useState("");
    const [step, setStep] = useState("initial");
    const [message, setMessage] = useState("");
    const navigate = useNavigate(); // Hook for navigation

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

    const handleGenerateMinutes = async () => {
        setStep("processing");
        setMessage("Generating minutes...");
        try {
            // MODIFIED: Call the new endpoint
            await api.post("/generate-minutes");
            setStep("done");
            setMessage("🎉 Minutes generated successfully! You can now view them on the 'My Minutes' page.");
        } catch (error) {
            console.error("Processing failed:", error);
            setStep("transcribed");
            setMessage(`❌ Minutes generation failed: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleFinishAndNavigate = () => {
        handleClose();
        navigate("/minutes"); // Navigate to the new minutes page
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
                    <button onClick={handleGenerateMinutes} className="form-submit-btn">
                        Generate Minutes
                    </button>
                )}

                {step === "processing" && <div className="loader"></div>}

                {step === "done" && (
                    <button onClick={handleFinishAndNavigate} className="form-submit-btn">
                        View Minutes
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