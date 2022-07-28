import "./App.css";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import apex_logo from "./resources/Apex_Logo_Final.png";
import UserForm from "./UserForm";
import PieResults from "./PieResults";
import Login from "./Login";
import { StrictMode } from "react";
import { AuthProvider } from "./contexts/AuthContext";
import PrivateRoute from "./PrivateRoute";
import Profile from "./Profile";
import ResourcesFaq from "./ResourcesFaq";
import Signup from "./Signup";
import ForgotPassword from "./ForgotPassword";

function App() {
  return (
    <div className="App">
      <StrictMode>
        <Router>
          <AuthProvider>
            <header>
              <Link to="/">
                <img src={apex_logo} alt="" />
              </Link>
            </header>

            <Switch>
              {/* User can't access UserForm until they have logged in. This re-directs them to Login if signed out. */}
              <PrivateRoute exact path="/">
                <UserForm />
              </PrivateRoute>

              <Route path="/pieresults">
                <PieResults />
              </Route>

              <Route path="/login">
                <Login />
              </Route>

              <Route path="/signup">
                <Signup />
              </Route>

              <Route path="/forgot-password">
                <ForgotPassword />
              </Route>

              {/* User can't access Profile info until they have logged in. This re-directs them to Login if signed out. */}
              <PrivateRoute path="/profile">
                <Profile />
              </PrivateRoute>

              <Route path="/resourcesfaq">
                <ResourcesFaq />
              </Route>
            </Switch>
          </AuthProvider>
        </Router>
      </StrictMode>
    </div>
  );
}

export default App;
