import { createContext, useState, useContext } from 'react';

const AutomationContext = createContext();

export function useAutomation() {
    return useContext(AutomationContext);
}

export function AutomationProvider({ children }) {
    const [status, setStatus] = useState('idle'); // idle, running, success, error
    const [message, setMessage] = useState('');
    const [meetingId, setMeetingId] = useState(null);

    const startAutomation = (id, startMessage) => {
        setMeetingId(id);
        setStatus('running');
        setMessage(startMessage);
    };

    const updateAutomation = (newMessage) => {
        if (status === 'running') {
            setMessage(newMessage);
        }
    };
    
    const endAutomation = (endStatus, endMessage) => {
        setStatus(endStatus); // 'success' or 'error'
        setMessage(endMessage);
        // After a delay, reset to idle
        setTimeout(() => {
            setStatus('idle');
            setMessage('');
            setMeetingId(null);
        }, 5000);
    };

    const value = {
        status,
        message,
        meetingId,
        startAutomation,
        updateAutomation,
        endAutomation,
    };

    return (
        <AutomationContext.Provider value={value}>
            {children}
        </AutomationContext.Provider>
    );
}