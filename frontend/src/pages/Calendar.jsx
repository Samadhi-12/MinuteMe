import { useState, useEffect } from "react";
import { Calendar as BigCalendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import api from "../lib/axios";
import "../App.css";

const localizer = momentLocalizer(moment);

function eventStyleGetter(event) {
    // Meetings: blue, Action Items: green/yellow/red based on status
    if (event.resource?.type === "meeting") {
        return {
            style: {
                backgroundColor: "#3b82f6",
                color: "#fff",
                borderRadius: "8px",
                border: "none",
                fontWeight: 600,
                boxShadow: "0 2px 8px rgba(59,130,246,0.15)"
            }
        };
    }
    if (event.resource?.type === "action-item") {
        let bg = "#10b981"; // green for completed
        if (event.resource.status === "pending") bg = "#f59e0b"; // yellow
        if (event.resource.status === "in-progress") bg = "#3b82f6"; // blue
        if (event.resource.status === "overdue") bg = "#ef4444"; // red
        return {
            style: {
                backgroundColor: bg,
                color: "#fff",
                borderRadius: "8px",
                border: "none",
                fontWeight: 600,
                boxShadow: "0 2px 8px rgba(16,185,129,0.15)"
            }
        };
    }
    return {};
}

function Calendar() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                setLoading(true);
                const response = await api.get("/events");
                const formattedEvents = response.data.map((event) => ({
                    ...event,
                    start: new Date(event.start),
                    end: new Date(event.end),
                }));
                setEvents(formattedEvents);
            } catch (error) {
                console.error("Failed to fetch events:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchEvents();
    }, []);

    if (loading) {
        return <p>Loading calendar...</p>;
    }

    return (
        <div className="calendar-container dark-calendar">
            {/* Legend */}
            <div style={{
                marginBottom: "1em",
                display: "flex",
                gap: "2em",
                fontSize: "1em"
            }}>
                <span style={{ display: "flex", alignItems: "center", gap: "0.5em" }}>
                    <span style={{ width: 16, height: 16, background: "#3b82f6", borderRadius: 4, display: "inline-block" }}></span>
                    Meeting
                </span>
                <span style={{ display: "flex", alignItems: "center", gap: "0.5em" }}>
                    <span style={{ width: 16, height: 16, background: "#f59e0b", borderRadius: 4, display: "inline-block" }}></span>
                    Action Item (Pending)
                </span>
                <span style={{ display: "flex", alignItems: "center", gap: "0.5em" }}>
                    <span style={{ width: 16, height: 16, background: "#10b981", borderRadius: 4, display: "inline-block" }}></span>
                    Action Item (Completed)
                </span>
                <span style={{ display: "flex", alignItems: "center", gap: "0.5em" }}>
                    <span style={{ width: 16, height: 16, background: "#ef4444", borderRadius: 4, display: "inline-block" }}></span>
                    Action Item (Overdue)
                </span>
            </div>
            <BigCalendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{
                    height: "700px", // Make calendar taller
                    background: "var(--primary-dark)",
                    borderRadius: "12px",
                    boxShadow: "0 4px 24px rgba(59,130,246,0.08)",
                    padding: "2em",
                    color: "var(--text-primary)"
                }}
                eventPropGetter={eventStyleGetter}
                tooltipAccessor={event =>
                    event.resource?.type === "action-item"
                        ? `${event.title}\nOwner: ${event.resource.owner}\nStatus: ${event.resource.status}`
                        : event.title
                }
            />
        </div>
    );
}

export default Calendar;