import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const BackendURL = import.meta.env.VITE_BACKEND_URL;

export const Private = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetch(`${BackendURL}/api/userinfo`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Token inválido o expirado");
        return res.json();
      })
      .then((data) => {
        setUser(data.user);
      })
      .catch((err) => {
        console.error(err);
        setError("Sesión expirada o datos inválidos.");
        localStorage.removeItem("token");
        setTimeout(() => navigate("/login"), 1500);
      });
  }, []);

  return (
    <div className="container d-flex align-items-center justify-content-center min-vh-100">
      <div className="card shadow p-4" style={{ maxWidth: "500px", width: "100%" }}>
        <h2 className="text-center mb-4">Área Privada</h2>

        {error && <div className="alert alert-danger text-center">{error}</div>}

        {user ? (
          <div>
            <p className="text-muted text-center mb-3">
              ¡Bienvenido, <strong>{user.fullname}</strong>!
            </p>
            <ul className="list-group">
              <li className="list-group-item">
                <strong>ID:</strong> {user.id}
              </li>
              <li className="list-group-item">
                <strong>Nombre:</strong> {user.fullname}
              </li>
              <li className="list-group-item">
                <strong>Email:</strong> {user.email}
              </li>
              <li className="list-group-item">
                <strong>Activo:</strong> {user.is_active ? "Sí" : "No"}
              </li>
            </ul>
          </div>
        ) : (
          !error && <div className="text-center">Cargando usuario...</div>
        )}
      </div>
    </div>
  );
};
