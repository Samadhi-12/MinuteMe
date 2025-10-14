import { Crown, CheckCircle, MinusCircle } from "lucide-react";
import "../App.css";
import "../components/UI.css";

function Upgrade() {
  return (
    <div className="form-container upgrade-page">
      <div className="page-header" style={{ textAlign: "center" }}>
        <h2>
          <Crown size={32} style={{ color: "#f59e0b", verticalAlign: "middle" }} /> Upgrade to Premium
        </h2>
        <p className="subtitle">Unlock the full power of MinuteMe for your meetings</p>
      </div>
      <div className="upgrade-comparison">
        {/* Free Tier Card */}
        <div className="upgrade-card free-card">
          <h3>Free</h3>
          <ul className="feature-list">
            <li><CheckCircle size={18} className="feature-icon" /> Up to <strong>15 min</strong> meetings</li>
            <li><CheckCircle size={18} className="feature-icon" /> <strong>5 meetings</strong> per month</li>
            <li><CheckCircle size={18} className="feature-icon" /> Inbuilt calendar</li>
            <li><CheckCircle size={18} className="feature-icon" /> Manual processing</li>
            <li><CheckCircle size={18} className="feature-icon" /> View last <strong>3 meetings</strong></li>
            <li><CheckCircle size={18} className="feature-icon" /> In-app reminders</li>
            <li><MinusCircle size={18} className="feature-icon minus" /> Google Calendar integration</li>
            <li><MinusCircle size={18} className="feature-icon minus" /> Automation</li>
            <li><MinusCircle size={18} className="feature-icon minus" /> Email reminders</li>
            <li><MinusCircle size={18} className="feature-icon minus" /> Unlimited meeting history</li>
          </ul>
          <div className="upgrade-price">
            <span className="price-label">Free Forever</span>
          </div>
        </div>
        {/* Premium Tier Card */}
        <div className="upgrade-card premium-card">
          <h3>
            <Crown size={22} style={{ color: "#f59e0b", marginRight: 6 }} />
            Premium
          </h3>
          <ul className="feature-list">
            <li><CheckCircle size={18} className="feature-icon" /> <strong>1hr+</strong> meetings</li>
            <li><CheckCircle size={18} className="feature-icon" /> <strong>Unlimited</strong> meetings</li>
            <li><CheckCircle size={18} className="feature-icon" /> Google Calendar integration</li>
            <li><CheckCircle size={18} className="feature-icon" /> Automated processing</li>
            <li><CheckCircle size={18} className="feature-icon" /> Unlimited meeting history</li>
            <li><CheckCircle size={18} className="feature-icon" /> Email reminders</li>
            <li><CheckCircle size={18} className="feature-icon" /> All Free features included</li>
          </ul>
          <div className="upgrade-price">
            <span className="price-label premium">Just $9/month</span>
            <button className="primary-action-btn" style={{ marginTop: "1.5em", fontSize: "1.1em" }}>
              Upgrade Now
            </button>
          </div>
        </div>
      </div>
      <div className="upgrade-note">
        <p>
          <span style={{ color: "#f59e0b", fontWeight: 600 }}>Premium</span> unlocks unlimited meetings, automation, Google Calendar sync, and more.
        </p>
      </div>
    </div>
  );
}

export default Upgrade;