import React, { useRef, useState } from "react";

import { Card, Form, Button, Alert } from "react-bootstrap";

import { Link } from "react-router-dom";

import { useAuth } from "./contexts/AuthContext";

import { useHistory } from "react-router-dom";

const Login = () => {
  const emailRef = useRef();
  const passwordRef = useRef();
  const { login, currentUser } = useAuth();
  // default is "" so that we don't have an error by default
  const [error, setError] = useState("");
  const history = useHistory();

  async function handleSubmit(e) {
    e.preventDefault();

    console.log("Pressed.");

    // username/password sign-up is async b/c we are communicating with Firebase DB
    try {
      setError("");
      await login(emailRef.current.value, passwordRef.current.value);
      // re-direct to user profile after logging in
      history.push("/");
    } catch (e) {
      console.log(e);
      setError("Failed to log in to " + emailRef.current.value);
    }
  }

  return (
    <>
      <Card>
        <Card.Body>
          <h2>Log In</h2>
          {/* If there is a currentUser logged in, fetch the user's info from AuthContext and display it in the frontend. */}
          {currentUser &&
            "Current User: " + JSON.stringify(currentUser["email"])}
          {/* Display a small Error pop-up with the error message from handleSubmit() above. */}
          {error && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group id="email">
              <Form.Label>Email</Form.Label>
              <Form.Control type="email" ref={emailRef} required />
            </Form.Group>

            <Form.Group id="password">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" ref={passwordRef} required />
            </Form.Group>

            <Button type="Submit">
              Log In
            </Button>
          </Form>
        </Card.Body>
      </Card>

      <div>
        <Link to="forgot-password">
        Forgot Password?
        </Link>
      </div>

      <div>
        Need an account? <Link to="/signup">Sign Up.</Link>
      </div>
    </>
  );
};

export default Login;
