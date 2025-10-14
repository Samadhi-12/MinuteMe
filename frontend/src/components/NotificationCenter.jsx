import { useState, useEffect } from "react";
import { useUserRole } from "../hooks/useUserRole";
import { useAutomation } from "../context/AutomationContext"; // Import the automation context
import api from "../lib/axios";

function NotificationCenter() {
    const [notifications, setNotifications] = useState([]);
    const [showNotifications, setShowNotifications] = useState(false);
    const [unreadCount, setUnreadCount] = useState(0);
    const { isPremium } = useUserRole();
    const { startAutomation, updateAutomation, endAutomation } = useAutomation(); // Get automation functions
    
    useEffect(() => {
        fetchNotifications();
        // Poll for new notifications every 30 seconds
        const interval = setInterval(fetchNotifications, 30000);
        return () => clearInterval(interval);
    }, []);
    
    const fetchNotifications = async () => {
        try {
            const res = await api.get("/notifications");
            const newNotifications = res.data;
            setNotifications(newNotifications);
            setUnreadCount(newNotifications.filter(n => !n.read).length);

            // Check for automation updates
            const latestAutomationNotification = newNotifications
                .filter(n => n.related_id) // Filter for notifications tied to a process
                .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];

            if (latestAutomationNotification) {
                if (latestAutomationNotification.type === 'success') {
                    endAutomation('success', latestAutomationNotification.message);
                } else if (latestAutomationNotification.type === 'error') {
                    endAutomation('error', latestAutomationNotification.message);
                } else {
                    // It's a running process
                    updateAutomation(latestAutomationNotification.message);
                }
            }

        } catch (error) {
            console.error("Failed to fetch notifications:", error);
        }
    };
    
    const markAsRead = async (id) => {
        try {
            await api.patch(`/notifications/${id}/read`);
            setNotifications(notifications.map(n => 
                n.id === id ? { ...n, read: true } : n
            ));
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch (error) {
            console.error("Failed to mark notification as read:", error);
        }
    };
    
    const markAllAsRead = async () => {
        try {
            await api.post("/notifications/read-all");
            setNotifications(notifications.map(n => ({ ...n, read: true })));
            setUnreadCount(0);
        } catch (error) {
            console.error("Failed to mark all notifications as read:", error);
        }
    };
    
    return (
        <div className="notification-center">
            <button 
                className="notification-bell" 
                onClick={() => setShowNotifications(!showNotifications)}
            >
                🔔 {unreadCount > 0 && <span className="notification-badge">{unreadCount}</span>}
            </button>
            
            {showNotifications && (
                <div className="notification-dropdown">
                    <div className="notification-header">
                        <h3>Notifications</h3>
                        {unreadCount > 0 && (
                            <button className="mark-all-read" onClick={markAllAsRead}>
                                Mark all as read
                            </button>
                        )}
                    </div>
                    
                    <div className="notification-list">
                        {notifications.length > 0 ? (
                            notifications.map(notification => (
                                <div 
                                    key={notification.id}
                                    className={`notification-item ${!notification.read ? 'unread' : ''}`}
                                    onClick={() => markAsRead(notification.id)}
                                >
                                    <div className="notification-icon">
                                        {notification.type === 'meeting' ? '📅' : 
                                         notification.type === 'action' ? '✅' : '📝'}
                                    </div>
                                    <div className="notification-content">
                                        <p>{notification.message}</p>
                                        <span className="notification-time">
                                            {new Date(notification.created_at).toLocaleString()}
                                        </span>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="empty-notifications">
                                No notifications yet.
                            </div>
                        )}
                    </div>
                    
                    {!isPremium && (
                        <div className="notification-upgrade">
                            Upgrade to Premium for email notifications.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default NotificationCenter;