import { useState, useEffect } from "react";
import api from "../lib/axios"; // Use the authenticated api instance

function Agenda() {
  const [agendas, setAgendas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

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
            </div>
          ))}
        </div>
      ) : (
        <p>No agendas found. Go to "Create Agenda" to make one.</p>
      )}
    </div>
  );
}

export default Agenda;
