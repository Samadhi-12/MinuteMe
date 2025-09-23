import { useState, useEffect } from "react";
import { getAgenda, postTranscript } from "./api";
import "./App.css";

function App() {
  const [agenda, setAgenda] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [minutes, setMinutes] = useState(null);
  const [actionItems, setActionItems] = useState([]);

  // Load agenda on mount
  useEffect(() => {
    async function fetchAgenda() {
      const data = await getAgenda();
      setAgenda(data);
    }
    fetchAgenda();
  }, []);

  const handleGenerateMinutes = async () => {
    if (!transcript) return;
    const data = await postTranscript(transcript);
    setMinutes(data.minutes);
    setActionItems(data.action_items);
  };

  return (
    <div className="App">
      <h1>MinuteMe Dashboard</h1>

      <section>
        <h2>Agenda</h2>
        {agenda ? (
          <ul>
            {agenda.agenda.map((item, idx) => (
              <li key={idx}>
                {item.topic} - {item.priority} ({item.time_allocated})
              </li>
            ))}
          </ul>
        ) : (
          <p>Loading agenda...</p>
        )}
      </section>

      <section>
        <h2>Enter Transcript</h2>
        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          rows={6}
          cols={60}
        />
        <br />
        <button onClick={handleGenerateMinutes}>Generate Minutes & Action Items</button>
      </section>

      {minutes && (
        <section>
          <h2>Minutes</h2>
          <pre>{JSON.stringify(minutes, null, 2)}</pre>
        </section>
      )}

      {actionItems.length > 0 && (
        <section>
          <h2>Action Items</h2>
          <ul>
            {actionItems.map((item, idx) => (
              <li key={idx}>
                {item.task} - {item.owner} - {item.deadline}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

export default App;
