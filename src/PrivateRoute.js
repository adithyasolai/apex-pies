import React, {Component} from 'react'
import { Redirect } from 'react-router-dom'
import { Route } from "react-router-dom"
import {useAuth} from "./contexts/AuthContext"


// Makes sure that Profile page can only be accessed if we are currently logged into a user
// `children` are the actual components that need to be rendered on Profile page
export default function PrivateRoute({children, ...rest}) {
  const {currentUser} = useAuth()

  return (
    <Route
      {...rest}
      render = {() => {
        return currentUser ? children : <Redirect to='login'/>
      }
      }
    />
    
  )
}
