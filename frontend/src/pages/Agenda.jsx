import { useState, useEffect } from "react";
import api from "../lib/axios";
import AgendaForm from "../components/AgendaForm";

function Agenda() {
  const [agendas, setAgendas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [editAgenda, setEditAgenda] = useState(null);

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
  };

  const handleEditSubmit = async (payload, setMessage) => {
    try {
      const agendaItems = [
        ...payload.topics.map(topic => ({
          topic,
          priority: "info",
          time_allocated: "10 mins"
        })),
        ...payload.discussion_points.map(point => ({
          topic: point,
          priority: "discussion",
          time_allocated: "10 mins"
        }))
      ];

      const updatedAgenda = {
        meeting_name: payload.meeting_name || "Meeting",
        meeting_date: payload.date,
        agenda: agendaItems
      };

      await api.patch(`/agenda/${editAgenda.meeting_id}`, updatedAgenda);
      setMessage("Agenda updated!");
      setEditAgenda(null);
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
        <div className="grid-container">
          {agendas.map((agenda) => (
            <div key={agenda.meeting_id} className="card agenda-card">
              <div className="card-header">
                <h3>{agenda.meeting_name}</h3>
                <span className="card-date">{agenda.meeting_date}</span>
              </div>
              <div className="agenda-meta">
                <span className="agenda-count">{agenda.agenda?.length || 0} items</span>
                <span className="agenda-created">
                  Created: {agenda.created_at ? new Date(agenda.created_at).toLocaleDateString() : "N/A"}
                </span>
              </div>
              <div className="agenda-items-list">
                {agenda.agenda?.length > 0 ? (
                  <ul>
                    {agenda.agenda.map((item, idx) => (
                      <li key={idx} className="agenda-item">
                        <span className="agenda-topic">{item.topic}</span>
                        <span className={`agenda-priority badge-${item.priority}`}>{item.priority}</span>
                        <span className="agenda-time">{item.time_allocated}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No agenda items.</p>
                )}
              </div>
              <div className="card-actions">
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
            <AgendaForm
              initialValues={{
                meeting_name: editAgenda.meeting_name,
                date: editAgenda.meeting_date,
                topics: editAgenda.agenda?.map(item => item.topic) || [],
                discussion_points: editAgenda.agenda?.map(item => item.discussion_point).filter(Boolean) || [],
              }}
              mode="edit"
              onSubmit={handleEditSubmit}
              onCancel={() => setEditAgenda(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Agenda;
