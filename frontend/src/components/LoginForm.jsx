import { useState } from "react";
import { login } from "../services/api";

export default function LoginForm({ onSwitch, onSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin() {
    try {
      setLoading(true);
      setError("");
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      onSuccess(data.access_token);

    } catch (e) {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <h2>Login</h2>

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

      <button className="primary-btn" onClick={handleLogin} disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>

      <p className="tiny">
        Don’t have an account?{" "}
        <span className="link" onClick={onSwitch}>
          Sign up
        </span>
      </p>
    </>
  );
}
