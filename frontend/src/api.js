import api from "./lib/axios";

export const getAgenda = async () => {
  const res = await api.get("/agenda");
  return res.data;
};

export const postTranscript = async (transcript) => {
  // POST to /minutes and /action-items (when available)
  // For now, only /action-items is implemented in backend
  const actionRes = await api.post("/action-items", { text: transcript });
  // minutes endpoint is commented out in backend, so return dummy
  return {
    minutes: {},
    action_items: actionRes.data.action_items || [],
  };
};

// NEW: Create a new agenda
export const postAgenda = async (agendaData) => {
  const res = await api.post("/agenda", agendaData);
  return res.data;
};
