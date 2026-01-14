import { useState } from "react";
import { signup } from "../services/api";

export default function SignupForm({ onSwitch, onSuccess }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSignup() {
    try {
      setLoading(true);
      setError("");
      await signup(username, email, password);
      onSuccess();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <h2>Create account</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      {error && <p className="error">{error}</p>}

      <button className="primary-btn" onClick={handleSignup} disabled={loading}>
        {loading ? "Creating..." : "Sign up"}
      </button>

      <p className="tiny">
        Already have an account?{" "}
        <span className="link" onClick={onSwitch}>
          Login
        </span>
      </p>
    </>
  );
}
