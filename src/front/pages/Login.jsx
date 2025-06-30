import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const BackendURL = import.meta.env.VITE_BACKEND_URL;


export const Login = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
    const resp = await fetch(`${BackendURL}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        });

      if (!resp.ok) {
        const data = await resp.json();
        throw new Error(data.msg || "Error al iniciar sesión");
      }

      const data = await resp.json();
      localStorage.setItem("token", data.token);
      navigate("/private");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Iniciar Sesión</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Correo"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br />
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
};