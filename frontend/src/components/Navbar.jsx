export default function Navbar({ user, onLogin, onSignup, onLogout, onPricing }) {
  return (
    <nav className="navbar">
      <div className="logo">PolymathAI</div>

      <div className="nav-links">
        <span>How it works</span>
        <span className="link" onClick={onPricing}>Pricing</span>
      </div>

      <div className="auth-links">
        {user ? (
          <>
            <span className="username">👋 {user.username}</span>
            <button className="btn btn-login" onClick={onLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <button className="btn btn-login" onClick={onLogin}>
              Login
            </button>
            <button className="btn btn-login" onClick={onSignup}>
              Sign up
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
