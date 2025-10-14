import { Routes, Route } from "react-router-dom";
import {
  SignedIn,
  SignedOut,
  RedirectToSignIn,
  SignIn,
  SignUp,
  UserButton,
  useAuth, // Import useAuth
} from "@clerk/clerk-react";
import { useEffect } from "react"; // Import useEffect
import { setupAxiosInterceptors } from "./lib/axios"; // Import the setup function

import Dashboard from "./pages/Dashboard";
import Agenda from "./pages/Agenda";
import Minutes from "./pages/Minutes";
import MinuteDetail from "./pages/MinuteDetail"; // Import the new detail page
import ActionItems from "./pages/ActionItems";
import History from "./pages/History";
import Settings from "./pages/Settings";
import CreateAgenda from "./pages/CreateAgenda";
import Calendar from "./pages/Calendar"; // Import the new Calendar page
import Transcripts from "./pages/Transcripts";
import Navbar from "./components/Navbar";
import "./App.css";
import "./components/UI.css";

function App() {
  const { getToken } = useAuth();

  // Setup Axios interceptor when the component mounts
  useEffect(() => {
    setupAxiosInterceptors(getToken);
  }, [getToken]);

  return (
    <div className="App">
      <header>
        <SignedIn>
          <Navbar />
        </SignedIn>
      </header>
      <main>
        <Routes>
          <Route
            path="/sign-in/*"
            element={<SignIn routing="path" path="/sign-in" />}
          />
          <Route
            path="/sign-up/*"
            element={<SignUp routing="path" path="/sign-up" />}
          />
          <Route
            path="/"
            element={
              <>
                <SignedIn>
                  <Dashboard />
                </SignedIn>
                <SignedOut>
                  <RedirectToSignIn />
                </SignedOut>
              </>
            }
          />
          <Route
            path="/create-agenda"
            element={
              <SignedIn>
                <CreateAgenda />
              </SignedIn>
            }
          />
          <Route
            path="/agenda"
            element={
              <SignedIn>
                <Agenda />
              </SignedIn>
            }
          />
          <Route
            path="/calendar"
            element={
              <SignedIn>
                <Calendar />
              </SignedIn>
            }
          />
          <Route
            path="/minutes"
            element={
              <SignedIn>
                <Minutes />
              </SignedIn>
            }
          />
          <Route
            path="/minutes/:id" // Add route for specific minute
            element={
              <SignedIn>
                <MinuteDetail />
              </SignedIn>
            }
          />
          <Route
            path="/action-items"
            element={
              <SignedIn>
                <ActionItems />
              </SignedIn>
            }
          />
          <Route
            path="/history"
            element={
              <SignedIn>
                <History />
              </SignedIn>
            }
          />
          <Route
            path="/settings"
            element={
              <SignedIn>
                <Settings />
              </SignedIn>
            }
          />
          <Route
            path="/transcripts"
            element={
              <SignedIn>
                <Transcripts />
              </SignedIn>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
