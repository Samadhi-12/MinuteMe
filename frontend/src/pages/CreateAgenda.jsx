import AgendaForm from "../components/AgendaForm";
import api from "../lib/axios";

function CreateAgenda() {
    const handleCreate = async (payload, setMessage) => {
        try {
            await api.post("/agenda", payload);
            setMessage("Agenda created successfully!");
        } catch (err) {
            setMessage("Error creating agenda. Try again.");
        }
    };

    return (
        <div className="form-container">
            <h2>Create New Agenda</h2>
            <AgendaForm initialValues={{}} onSubmit={handleCreate} mode="create" />
        </div>
    );
}

export default CreateAgenda;
