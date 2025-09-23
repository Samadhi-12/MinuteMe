export const getAgenda = async () => {
  const response = await fetch("http://127.0.0.1:8000/agenda");
  return await response.json();
};

export const postTranscript = async (transcript) => {
  const response = await fetch("http://127.0.0.1:8000/minutes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transcript }),
  });
  return await response.json();
};
