export default function PricingModal({ open, onClose }) {
  if (!open) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal pricing-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="close-btn" onClick={onClose}>✕</button>

        <h2 className="pricing-title">Upgrade to Premium</h2>
        <p className="pricing-subtitle">
          Create better content, faster — without limits.
        </p>

        <div className="pricing-card">
          <div className="badge">Most Popular</div>

          <h3 className="plan-name">Creator</h3>

          <div className="price">
            <span className="amount">$3.99</span>
            <span className="period">/ month</span>
          </div>

          <ul className="features">
            <li>✔️ 100 short videos / month</li>
            <li>✔️ 30 long videos / month</li>
            <li>✔️ AI titles, descriptions & hashtags</li>
            <li>✔️ Priority processing</li>
            <li>✔️ No daily limits</li>
          </ul>

          <button className="primary-btn disabled">
            Coming soon
          </button>

          {/* <p className="tiny muted">
            Payments will be enabled soon
          </p> */}
        </div>

        <p className="pricing-footer">
          Cancel anytime · No hidden charges
        </p>
      </div>
    </div>
  );
}
