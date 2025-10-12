import { useState } from "react";
import { postAgenda } from "../api";

function CreateAgenda() {
  const [title, setTitle] = useState("");
  const [date, setDate] = useState("");
  const [attendees, setAttendees] = useState("");
  const [agendaItems, setAgendaItems] = useState([{ topic: "", priority: "", time_allocated: "" }]);
  const [message, setMessage] = useState("");

  const handleItemChange = (index, field, value) => {
    const items = [...agendaItems];
    items[index][field] = value;
    setAgendaItems(items);
  };

  const handleAddItem = () => setAgendaItems([...agendaItems, { topic: "", priority: "", time_allocated: "" }]);
  const handleRemoveItem = (index) => {
    const items = agendaItems.filter((_, idx) => idx !== index);
    setAgendaItems(items.length ? items : [{ topic: "", priority: "", time_allocated: "" }]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      title,
      date,
      attendees: attendees.split(",").map(a => a.trim()).filter(a => a),
      agenda: agendaItems.filter(item => item.topic),
    };
    try {
      await postAgenda(payload);
      setMessage("Agenda created successfully!");
      setTitle(""); setDate(""); setAttendees(""); setAgendaItems([{ topic: "", priority: "", time_allocated: "" }]);
    } catch (err) {
      console.error(err);
      setMessage("Error creating agenda. Try again.");
    }
  };

  return (
    <div>
      <h2>Create New Agenda</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title: </label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Date: </label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        </div>
        <div>
          <label>Attendees (comma separated): </label>
          <input type="text" value={attendees} onChange={(e) => setAttendees(e.target.value)} />
        </div>

        <h3>Agenda Items</h3>
        {agendaItems.map((item, idx) => (
          <div key={idx} style={{ marginBottom: "0.5em" }}>
            <input type="text" placeholder="Topic" value={item.topic} onChange={(e) => handleItemChange(idx, "topic", e.target.value)} style={{ marginRight: "0.5em" }} />
            <input type="text" placeholder="Priority" value={item.priority} onChange={(e) => handleItemChange(idx, "priority", e.target.value)} style={{ marginRight: "0.5em" }} />
            <input type="text" placeholder="Time Allocated" value={item.time_allocated} onChange={(e) => handleItemChange(idx, "time_allocated", e.target.value)} style={{ marginRight: "0.5em" }} />
            <button type="button" onClick={() => handleRemoveItem(idx)}>Remove</button>
          </div>
        ))}
        <button type="button" onClick={handleAddItem}>Add Agenda Item</button>
        <br /><br />
        <button type="submit">Create Agenda</button>
      </form>
    </div>
  );
}

export default CreateAgenda;
