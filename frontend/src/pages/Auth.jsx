import { useState } from "react";
import "./Auth.css";

export default function Auth() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    setError("");

    const payload = isRegister
      ? { email, password, name }
      : { email, password };

    const url = isRegister
      ? "http://127.0.0.1:8000/api/auth/register"
      : "http://127.0.0.1:8000/api/auth/login";

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Authentication failed");
        return;
      }

      if (!isRegister) {
        localStorage.setItem("token", data.token);
        window.location.href = "/dashboard";
      } else {
        setIsRegister(false);
      }

    } catch (err) {
      setError("Server not reachable");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>{isRegister ? "Create Account" : "Welcome Back"}</h2>

        {isRegister && (
          <input
            placeholder="Name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        {error && <p className="error">{error}</p>}

        <button onClick={submit}>
          {isRegister ? "Register" : "Login"}
        </button>

        <p className="switch" onClick={() => setIsRegister(!isRegister)}>
          {isRegister
            ? "Already have an account? Login"
            : "New here? Register"}
        </p>
      </div>
    </div>
  );
}
