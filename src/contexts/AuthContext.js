import React, { useContext, useState, useEffect } from "react";
import { database, auth } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail
} from "firebase/auth";

import { ref, set } from "firebase/database";

const AuthContext = React.createContext();

// allows access to using this context
export function useAuth() {
  return useContext(AuthContext);
}

// creates the context
export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(auth.currentUser);
  const [loading, setLoading] = useState(true);

  function signup(email, password) {
    // Returns a "Promise" (a response from Firebase API that we can await)
    return createUserWithEmailAndPassword(auth, email, password).then(
      (userCredential) => {
        console.log("Made account for ", userCredential.user.email);
        const userDataJSON = { email: userCredential.user.email };

        // Initialize this new user in the Firebase RTDB
        try {
          // TODO: Create a new, protected user in Authentication. Make Firebase rule so that only
          // that user can write to the DB. Change to that user before this write because
          // createUserWithEmailAndPassword overwrites the existing user
          set(ref(database, "users/" + userCredential.user.uid), userDataJSON);
          console.log(
            "Initialized Account Info in RTDB for ",
            userCredential.user.email
          );
        } catch (e) {
          console.log(e);
        }
      }
    );
  }

  function resetPassword(email) {
    return sendPasswordResetEmail(auth, email)

  }

  function login(email, password) {
    return signInWithEmailAndPassword(auth, email, password).then(
      (userCredential) => {
        console.log("Logged into ", userCredential.user.email);
      }
    );
  }

  function signout() {
    return signOut(auth);
  }

  // do this every time the currentUser changes!
  useEffect(() => {
    // triggers automatically when a username+password is set in Firebase
    // Puts the newly authenticated user as the currentUser in our Context.
    // TODO: REMOVE THIS, WE SHOULD MAKE USER LOG-IN AGAIN TO SET THE CONTEXT
    // THIS `unsubscribe` VARIABLE NAME HAS NOTHING TO DO WITH ACTUALLY CLOSING A USER ACCOUNT
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setCurrentUser(user);
      setLoading(false);
    });

    console.log("Set currentUser to: ", currentUser);

    // Not really sure why this return is needed, since this is just a side-effect function, and
    // no code is waiting for the return value of this function.
    return unsubscribe;
  }, [currentUser]);

  // `value` contains all the information we want to provide with our authentication.
  const value = {
    currentUser,
    signup,
    login,
    signout,
    resetPassword
  };

  return (
    <AuthContext.Provider value={value}>
      {/* Only load children if loading=false, meaning only if we have a currentUser loaded */}
      {!loading && children}
    </AuthContext.Provider>
  );
}
