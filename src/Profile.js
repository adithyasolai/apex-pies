import React, {useState} from 'react'
import {useAuth} from './contexts/AuthContext'
import {Card, Button, Alert} from 'react-bootstrap'
import { Link } from 'react-router-dom';
import { useHistory } from 'react-router-dom';

export default function Profile() {
  const {currentUser, signout} = useAuth();
  const [error, setError] = useState("")
  const history = useHistory();

  async function handleSignOut(e) {
    e.preventDefault();

    console.log("Pressed.")

    setError("")

    // username/password sign-up is async b/c we are communicating with Firebase DB
    try {
      await signout()
      // re-direct to log-in after sign-out
      history.push("/login")
    } catch(err) {
      console.log(err)
      setError("Failed to sign out.")
    }
  }

  return (
    <div>
      <Card>
        <Card.Body>
          <h2 className='text-center mb-4'>Profile</h2>
          {currentUser && <h3 className='text-center mb-4'>Current User: {currentUser['email']}</h3>}
          {error && <Alert variant='danger'>{error}</Alert>}
          <Link to="/update-profile" className='btn btn-primary w-100 mt-3'> Update Profile </Link>
        </Card.Body>

      </Card>

      <div className='w-100 text-center mt-2'>
        <Button variant='link' onClick={handleSignOut} > Sign Out </Button>
      </div>
      
    </div>
  )
}
