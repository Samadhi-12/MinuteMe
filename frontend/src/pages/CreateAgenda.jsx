import { useState } from "react";
import api from "../lib/axios";

function CreateAgenda() {
    const [date, setDate] = useState("");
    const [topics, setTopics] = useState([{ id: 1, value: "" }]);
    const [discussionPoints, setDiscussionPoints] = useState([{ id: 1, value: "" }]);
    const [message, setMessage] = useState("");

    const handleItemChange = (id, value, itemType) => {
        const setter = itemType === "topic" ? setTopics : setDiscussionPoints;
        setter((prevItems) =>
            prevItems.map((item) => (item.id === id ? { ...item, value } : item))
        );
    };

    const addItem = (itemType) => {
        const setter = itemType === "topic" ? setTopics : setDiscussionPoints;
        setter((prevItems) => [...prevItems, { id: Date.now(), value: "" }]);
    };

    const removeItem = (id, itemType) => {
        const setter = itemType === "topic" ? setTopics : setDiscussionPoints;
        setter((prevItems) => prevItems.filter((item) => item.id !== id));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const payload = {
            topics: topics.map((t) => t.value).filter(Boolean),
            discussion_points: discussionPoints.map((dp) => dp.value).filter(Boolean),
            date: date,
        };

        if (payload.topics.length === 0 && payload.discussion_points.length === 0) {
            setMessage("Please add at least one topic or discussion point.");
            return;
        }

        try {
            await api.post("/agenda", payload);
            setMessage("Agenda created successfully!");
            // Reset form
            setDate("");
            setTopics([{ id: 1, value: "" }]);
            setDiscussionPoints([{ id: 1, value: "" }]);
        } catch (err) {
            console.error(err);
            setMessage("Error creating agenda. Try again.");
        }
    };

    return (
        <div className="form-container">
            <h2>Create New Agenda</h2>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="date">Meeting Date</label>
                    <input
                        id="date"
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Topics</label>
                    {topics.map((topic, index) => (
                        <div key={topic.id} className="form-item-group">
                            <input
                                type="text"
                                placeholder={`Topic ${index + 1}`}
                                value={topic.value}
                                onChange={(e) => handleItemChange(topic.id, e.target.value, "topic")}
                            />
                            {topics.length > 1 && (
                                <button
                                    type="button"
                                    className="item-btn remove-btn"
                                    onClick={() => removeItem(topic.id, "topic")}
                                >
                                    -
                                </button>
                            )}
                        </div>
                    ))}
                    <button type="button" className="item-btn add-item-btn" onClick={() => addItem("topic")}>
                        + Add Topic
                    </button>
                </div>

                <div className="form-group">
                    <label>Discussion Points</label>
                    {discussionPoints.map((point, index) => (
                        <div key={point.id} className="form-item-group">
                            <input
                                type="text"
                                placeholder={`Discussion Point ${index + 1}`}
                                value={point.value}
                                onChange={(e) => handleItemChange(point.id, e.target.value, "discussion")}
                            />
                            {discussionPoints.length > 1 && (
                                <button
                                    type="button"
                                    className="item-btn remove-btn"
                                    onClick={() => removeItem(point.id, "discussion")}
                                >
                                    -
                                </button>
                            )}
                        </div>
                    ))}
                    <button type="button" className="item-btn add-item-btn" onClick={() => addItem("discussion")}>
                        + Add Discussion Point
                    </button>
                </div>

                <button type="submit" className="form-submit-btn">
                    Create Agenda
                </button>
            </form>
        </div>
    );
}

export default CreateAgenda;
