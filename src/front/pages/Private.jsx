import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const BackendURL = import.meta.env.VITE_BACKEND_URL;

export const Private = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetch(`${BackendURL}/api/private`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Token inválido");
        return res.json();
      })
      .then((data) => setMessage(data.msg))
      .catch((err) => {
        console.error(err);
        localStorage.removeItem("token");
        navigate("/login");
      });
  }, []);

  return (
    <div>
      <h1>Área privada</h1>
      <p>{message}</p>
    </div>
  );
};

