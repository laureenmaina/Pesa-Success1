import React, { useState } from "react";

import { useHistory } from 'react-router-dom';

function Login({ setUser }) {

  const history = useHistory();

  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  function handleChange(e) {
    const { id, value } = e.target;
    setCredentials((prev) => ({ ...prev, [id]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    setError(""); // Reset error message

    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((user) => {
            setUser(user);
            history.push("/");
          });
        } else {
          setError("Invalid username or password. Please signup if you haven't already");
        }
      })
      .catch((error) => {
        console.error("Error during login:", error);
        setError("An unexpected error occurred. Please try again.");
      });
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>Login</h1>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <label className="labels" htmlFor="username">Username</label>
        <input
          className="inputfields"
          type="text"
          id="username"
          autoComplete="off"
          value={credentials.username}
          onChange={handleChange}
        />
        <label className="labels" htmlFor="password">Password</label>
        <input
          className="inputfields"
          type="password"
          id="password"
          autoComplete="current-password"
          value={credentials.password}
          onChange={handleChange}
        />
        <button className="submitbtns" type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
