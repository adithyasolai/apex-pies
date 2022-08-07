import React, { useRef, useState } from "react";

import { Card, Form, Button, Alert } from "react-bootstrap";

import { useAuth } from "./contexts/AuthContext";

import { Link, useHistory } from "react-router-dom";

const Signup = () => {
  const emailRef = useRef();
  const passwordRef = useRef();
  const passwordConfirmRef = useRef();
  const { signup, currentUser } = useAuth();
  // default is "" so that we don't have an error by default
  const [error, setError] = useState("");
  // TODO - implement loading
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  async function handleSubmit(e) {
    e.preventDefault();

    console.log("Pressed.");

    if (passwordRef.current.value !== passwordConfirmRef.current.value) {
      console.log("Passwords do not match.");
      return setError("Passwords do not match.");
    }

    // username/password sign-up is async b/c we are communicating with Firebase DB
    try {
      setError("");
      setLoading(true);
      await signup(emailRef.current.value, passwordRef.current.value);
      // re-direct to user profile after signin up
      history.push("/profile");
    } catch (e) {
      console.log(e);
      setError("Failed to create an account.");
    }

    setLoading(false);
  }

  return (
    <>
      <Card>
        <Card.Body>
          <h2>Sign Up</h2>
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

            <Form.Group id="password-confirm">
              <Form.Label>Password Confirmation</Form.Label>
              <Form.Control type="password" ref={passwordConfirmRef} required />
            </Form.Group>

            <Button type="Submit">
              Sign Up
            </Button>
          </Form>
        </Card.Body>
      </Card>
      <div>
        Already have an account? <Link to="/login">Log In.</Link>
      </div>
    </>
  );
};

export default Signup;
