import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Agenda from "./pages/Agenda";
import Minutes from "./pages/Minutes";
import ActionItems from "./pages/ActionItems";
import History from "./pages/History";
import Settings from "./pages/Settings";
import CreateAgenda from "./pages/CreateAgenda";
import Navbar from "./components/Navbar";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/create-agenda" element={<CreateAgenda />} />
            <Route path="/agenda" element={<Agenda />} />
            <Route path="/minutes" element={<Minutes />} />
            <Route path="/action-items" element={<ActionItems />} />
            <Route path="/history" element={<History />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
