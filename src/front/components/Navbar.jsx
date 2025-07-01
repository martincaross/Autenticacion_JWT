import React from "react";
import { Link, useNavigate } from "react-router-dom";

export const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">
          Home
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContent"
          aria-controls="navbarContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className="collapse navbar-collapse" id="navbarContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {token && (
              <li className="nav-item">
                <Link className="nav-link" to="/private">
                  Área privada
                </Link>
              </li>
            )}
          </ul>

          <div className="d-flex">
            {token ? (
              <button className="btn btn-outline-light" onClick={handleLogout}>
                Cerrar sesión
              </button>
            ) : (
              <>
                <Link to="/login" className="btn btn-outline-light me-2">
                  Iniciar sesión
                </Link>
                <Link to="/signup" className="btn btn-primary">
                  Registrarse
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
