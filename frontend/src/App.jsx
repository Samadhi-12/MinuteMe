import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Agenda from "./pages/Agenda";
import Minutes from "./pages/Minutes";
import ActionItems from "./pages/ActionItems";
import History from "./pages/History";
import Settings from "./pages/Settings";
import CreateAgenda from "./pages/CreateAgenda";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul style={{ display: "flex", gap: "1em", listStyle: "none" }}>
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/create-agenda">Create Agenda</Link></li>
            <li><Link to="/agenda">Agenda</Link></li>
            <li><Link to="/minutes">Minutes</Link></li>
            <li><Link to="/action-items">Action Items</Link></li>
            <li><Link to="/history">History</Link></li>
            <li><Link to="/settings">Settings</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/create-agenda" element={<CreateAgenda />} />
          <Route path="/agenda" element={<Agenda />} />
          <Route path="/minutes" element={<Minutes />} />
          <Route path="/action-items" element={<ActionItems />} />
          <Route path="/history" element={<History />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
