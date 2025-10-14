import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom"; // Import useNavigate
import api from "../lib/axios";
import AnalyzeMeetingModal from "../components/AnalyzeMeetingModal";
import { formatDateRelative, formatMeetingId } from "../utils/formatters";
import { useUserRole } from "../hooks/useUserRole";
import ProcessingModeToggle from "../components/ProcessingModeToggle"; // Import the new component

function Dashboard() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [recentMinutes, setRecentMinutes] = useState([]);
    const [upcomingActions, setUpcomingActions] = useState([]);
    const [agendaCount, setAgendaCount] = useState(0);
    const [loading, setLoading] = useState(true);
    const [autoMode, setAutoMode] = useState(false);
    const { isPremium, tier } = useUserRole();
    const [automationQuota, setAutomationQuota] = useState(5);
    const navigate = useNavigate(); // Initialize useNavigate

    useEffect(() => {
        async function fetchDashboardData() {
            try {
                setLoading(true);
                
                // Get recent minutes
                const minutesRes = await api.get("/minutes");
                // Sort by date and take the first 3
                const sortedMinutes = minutesRes.data
                    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                    .slice(0, 3);
                setRecentMinutes(sortedMinutes);
                
                // Get upcoming action items
                const actionsRes = await api.get("/action-items");
                // Filter to only pending items and sort by deadline
                const pendingActions = actionsRes.data
                    .filter(item => item.status !== "completed")
                    .sort((a, b) => new Date(a.deadline) - new Date(b.deadline))
                    .slice(0, 5);
                setUpcomingActions(pendingActions);
                
                // Get agenda count
                const agendasRes = await api.get("/agendas");
                setAgendaCount(agendasRes.data.length);
                
                // Get automation quota for free users
                if (!isPremium) {
                    const quotaRes = await api.get("/user/automation-quota");
                    setAutomationQuota(quotaRes.data.remaining);
                }
                
            } catch (error) {
                console.error("Failed to fetch dashboard data", error);
            } finally {
                setLoading(false);
            }
        }
        
        fetchDashboardData();
    }, [isPremium]);

    const handleAnalyzeMeeting = () => {
        setIsModalOpen(true);
    };

    const handleCreateAgenda = () => {
        // Navigate to the agenda page and pass state to open the modal
        navigate('/agenda', { state: { openCreateModal: true } });
    };

    return (
        <div className="dashboard-container">
            <AnalyzeMeetingModal 
                isOpen={isModalOpen} 
                onClose={() => setIsModalOpen(false)} 
                autoMode={autoMode} // Pass autoMode to the modal
            />

            <header className="dashboard-header">
                <h1>Welcome to MinuteMe</h1>
                <p>Turn your meetings into actionable outcomes</p>
                <div className="header-actions">
                    <button
                        onClick={handleAnalyzeMeeting}
                        className="primary-action-btn"
                    >
                        ✨ Analyze New Meeting
                    </button>
                    {/* Change this from a Link to a button with an onClick handler */}
                    <button onClick={handleCreateAgenda} className="secondary-action-btn">
                        📝 Create New Agenda
                    </button>
                </div>
            </header>

            {/* Replace the old toggle with the new component */}
            <ProcessingModeToggle 
                autoMode={autoMode}
                setAutoMode={setAutoMode}
                isPremium={isPremium}
                automationQuota={automationQuota}
            />

            <div className="dashboard-stats">
                <div className="stat-card">
                    <div className="stat-number">{recentMinutes.length}</div>
                    <div className="stat-label">Recent Minutes</div>
                </div>
                <div className="stat-card">
                    <div className="stat-number">{upcomingActions.length}</div>
                    <div className="stat-label">Pending Actions</div>
                </div>
                <div className="stat-card">
                    <div className="stat-number">{agendaCount}</div>
                    <div className="stat-label">Created Agendas</div>
                </div>
            </div>

            <div className="dashboard-main-content">
                <section className="recent-meetings">
                    <div className="section-header">
                        <h2>Recent Minutes</h2>
                        <Link to="/minutes" className="view-all">View All</Link>
                    </div>
                    
                    {loading ? (
                        <div className="loading-container">
                            <div className="loader"></div>
                            <p>Loading recent meetings...</p>
                        </div>
                    ) : recentMinutes.length > 0 ? (
                        <div className="card-list">
                            {recentMinutes.map((minute) => (
                                <div key={minute._id} className="card meeting-card">
                                    <div className="card-header">
                                        <h3>{minute.meeting_name || formatMeetingId(minute.meeting_id)}</h3>
                                        <span className="date-badge">{formatDateRelative(minute.date)}</span>
                                    </div>
                                    <p className="card-summary">{minute.summary}</p>
                                    <Link to={`/minutes/${minute._id}`} className="card-link">
                                        View Details →
                                    </Link>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="empty-state">
                            <div className="empty-icon">📝</div>
                            <h3>No minutes yet</h3>
                            <p>Analyze a meeting to generate minutes</p>
                        </div>
                    )}
                </section>

                <aside className="upcoming-actions">
                    <div className="section-header">
                        <h2>Upcoming Action Items</h2>
                        <Link to="/action-items" className="view-all">View All</Link>
                    </div>
                    
                    {loading ? (
                        <div className="loading-container">
                            <div className="loader"></div>
                            <p>Loading action items...</p>
                        </div>
                    ) : upcomingActions.length > 0 ? (
                        <div className="action-item-list">
                            {upcomingActions.map((action) => (
                                <div key={action._id} className="card action-item-card">
                                    <p className="action-task">{action.task}</p>
                                    <div className="action-meta">
                                        <div className="due-date">
                                            <span className="label">Due:</span> 
                                            <span>{formatDateRelative(action.deadline)}</span>
                                        </div>
                                        <div className="owner">
                                            <span className="label">Owner:</span> 
                                            <span>{action.owner}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="empty-state">
                            <div className="empty-icon">✅</div>
                            <h3>No pending actions</h3>
                            <p>You're all caught up!</p>
                        </div>
                    )}
                </aside>
            </div>
        </div>
    );
}

export default Dashboard;
