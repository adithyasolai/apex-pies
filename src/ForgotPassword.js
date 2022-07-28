import React, { useRef, useState } from "react";

import { Card, Form, Button, Alert } from "react-bootstrap";

import { Link } from "react-router-dom";

import { useAuth } from "./contexts/AuthContext";


const ForgotPassword = () => {
  const emailRef = useRef();
  const { resetPassword, currentUser } = useAuth();
  // default is "" so that we don't have an error by default
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    console.log("Pressed.");

    // username/password sign-up is async b/c we are communicating with Firebase DB
    try {
      setMessage('')
      setError("");
      await resetPassword(emailRef.current.value);
      setMessage('Check inbox for further instructions!')
    } catch (e) {
      console.log(e);
      setError("Failed to reset password for " + emailRef.current.value);
    }
  }

  return (
    <>
      <Card>
        <Card.Body>
          <h2>Password Reset</h2>
          {/* If there is a currentUser logged in, fetch the user's info from AuthContext and display it in the frontend. */}
          {currentUser &&
            "Current User: " + JSON.stringify(currentUser["email"])}
          {/* Display a small Error pop-up with the error message from handleSubmit() above. */}
          {error && <Alert variant="danger">{error}</Alert>}
          {message && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group id="email">
              <Form.Label>Email</Form.Label>
              <Form.Control type="email" ref={emailRef} required />
            </Form.Group>

            <Button type="Submit">
              Send Reset Email
            </Button>
          </Form>
        </Card.Body>
      </Card>

      <div>
        <Link to="/login">
          Back to Login Page.
        </Link>
      </div>

      <div>
        Need an account? <Link to="/signup">Sign Up.</Link>
      </div>
    </>
  );
};

export default ForgotPassword;
