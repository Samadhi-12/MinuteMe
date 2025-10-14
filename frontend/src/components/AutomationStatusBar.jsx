import { useAutomation } from '../context/AutomationContext';
import './UI.css';

function AutomationStatusBar() {
    const { status, message } = useAutomation();

    if (status === 'idle') {
        return null;
    }

    return (
        <div className={`automation-status-bar status-${status}`}>
            {status === 'running' && <div className="status-loader"></div>}
            <p>{message}</p>
        </div>
    );
}

export default AutomationStatusBar;