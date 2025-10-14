import { Link } from "react-router-dom";

function ProcessingModeToggle({ autoMode, setAutoMode, isPremium, automationQuota }) {
    return (
        <div className="processing-mode">
            <h3>Processing Mode</h3>
            <div className="mode-toggle">
                <button
                    className={`mode-btn ${!autoMode ? 'active' : ''}`}
                    onClick={() => setAutoMode(false)}
                >
                    Manual
                </button>
                <button
                    className={`mode-btn ${autoMode ? 'active' : ''}`}
                    onClick={() => setAutoMode(true)}
                    disabled={!isPremium && automationQuota <= 0}
                >
                    Auto {!isPremium && `(${automationQuota} left)`}
                </button>
            </div>
            
            {!isPremium && automationQuota <= 2 && (
                <div className="quota-warning">
                    You have {automationQuota} automation cycle(s) left this month. 
                    <Link to="/upgrade" className="upgrade-link">Upgrade to Premium</Link>
                </div>
            )}
        </div>
    );
}

export default ProcessingModeToggle;