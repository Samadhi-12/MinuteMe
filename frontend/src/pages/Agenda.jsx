import { useState, useEffect } from "react";
import api from "../lib/axios";

function Agenda() {
  const [agendas, setAgendas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [editAgenda, setEditAgenda] = useState(null);
  const [editForm, setEditForm] = useState({ meeting_name: "", meeting_date: "", agenda: [] });

  useEffect(() => {
    async function fetchAgendas() {
      try {
        setLoading(true);
        const response = await api.get("/agendas");
        setAgendas(response.data);
      } catch (error) {
        console.error("Failed to fetch agendas", error);
      } finally {
        setLoading(false);
      }
    }
    fetchAgendas();
  }, []);

  const handleSchedule = async (agendaId) => {
    try {
      setMessage(`Scheduling ${agendaId}...`);
      await api.post("/schedule-agenda", { agenda_id: agendaId });
      setMessage(`Successfully scheduled meeting for ${agendaId}!`);
    } catch (error) {
      console.error("Failed to schedule agenda:", error);
      setMessage(`Error scheduling meeting: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleEdit = (agenda) => {
    setEditAgenda(agenda);
    setEditForm({
      meeting_name: agenda.meeting_name,
      meeting_date: agenda.meeting_date,
      agenda: agenda.agenda.map(item => ({ ...item }))
    });
  };

  const handleEditChange = (idx, field, value) => {
    setEditForm(form => ({
      ...form,
      agenda: form.agenda.map((item, i) => i === idx ? { ...item, [field]: value } : item)
    }));
  };

  const handleEditFormChange = (field, value) => {
    setEditForm(form => ({ ...form, [field]: value }));
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.patch(`/agenda/${editAgenda.meeting_id}`, editForm);
      setMessage("Agenda updated!");
      setEditAgenda(null);
      // Refresh agendas
      const response = await api.get("/agendas");
      setAgendas(response.data);
    } catch (err) {
      setMessage("Error updating agenda.");
    }
  };

  if (loading) return <p>Loading agendas...</p>;

  return (
    <div className="form-container">
      <h2>My Agendas</h2>
      {message && <p>{message}</p>}
      {agendas.length > 0 ? (
        <div className="card-list">
          {agendas.map((agenda) => (
            <div key={agenda.meeting_id} className="card">
              <h3>{agenda.meeting_name}</h3>
              <p className="card-date">{agenda.meeting_date}</p>
              <button 
                className="form-submit-btn" 
                style={{marginTop: '1em', width: 'auto', padding: '0.5em 1em'}}
                onClick={() => handleSchedule(agenda.meeting_id)}
              >
                Schedule Meeting
              </button>
              <button
                className="form-submit-btn"
                style={{marginTop: '1em', marginLeft: '1em', width: 'auto', padding: '0.5em 1em'}}
                onClick={() => handleEdit(agenda)}
              >
                Edit Agenda
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p>No agendas found. Go to "Create Agenda" to make one.</p>
      )}

      {/* Edit Modal */}
      {editAgenda && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Edit Agenda</h3>
            <form onSubmit={handleEditSubmit}>
              <div>
                <label>Meeting Name</label>
                <input
                  type="text"
                  value={editForm.meeting_name}
                  onChange={e => handleEditFormChange("meeting_name", e.target.value)}
                />
              </div>
              <div>
                <label>Meeting Date</label>
                <input
                  type="date"
                  value={editForm.meeting_date}
                  onChange={e => handleEditFormChange("meeting_date", e.target.value)}
                />
              </div>
              <div>
                <label>Agenda Items</label>
                {editForm.agenda.map((item, idx) => (
                  <div key={idx} style={{marginBottom: "0.5em"}}>
                    <input
                      type="text"
                      value={item.topic}
                      onChange={e => handleEditChange(idx, "topic", e.target.value)}
                      placeholder="Topic"
                    />
                    <select
                      value={item.priority}
                      onChange={e => handleEditChange(idx, "priority", e.target.value)}
                    >
                      <option value="urgent">Urgent</option>
                      <option value="discussion">Discussion</option>
                      <option value="info">Info</option>
                    </select>
                    <input
                      type="text"
                      value={item.time_allocated}
                      onChange={e => handleEditChange(idx, "time_allocated", e.target.value)}
                      placeholder="Time Allocated"
                    />
                  </div>
                ))}
              </div>
              <button type="submit" className="form-submit-btn">Save Changes</button>
              <button type="button" className="modal-close-btn" onClick={() => setEditAgenda(null)}>Cancel</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Agenda;
