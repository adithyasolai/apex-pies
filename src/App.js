import { Component } from "react";
import ReactDOM from "react-dom";
import { StrictMode } from "react";
import apex_logo from "../resources/Apex_Logo_Final.png";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import UserForm from "./UserForm";
import PieResults from "./PieResults";
import ResourcesFaq from "./ResourcesFaq";
import Signup from "./Signup";
import {Container} from 'react-bootstrap';
import {AuthProvider} from './contexts/AuthContext'

// enables Bootstrap CSS. but conflicts with existing CSS used.
// import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      
      <div>
        <Router>
          <AuthProvider>
          <header>
            <Link to="/">
              <img src={apex_logo} alt="" />
            </Link>
          </header>

          {/* Determines which page to serve. */}
          <Switch>
            <Route path="/pieresults">
              <PieResults />
            </Route>

            <Route path="/resourcesfaq">
              <ResourcesFaq />
            </Route>

            <Route path="/signup">
              <Container className="d-flex align-items-center justify-content-center" style={{minHeight: "100vh"}}>
                <div className='w-100' style={{maxWidth: "400px"}}>
                  <Signup />
                </div>
                
              </Container>
            </Route>

            <Route exact path="/">
              <UserForm />
            </Route>
          </Switch>
          </AuthProvider>
        </Router>
      </div>
    );
  }
}

ReactDOM.render(
  <StrictMode>
    <App />
  </StrictMode>,
  document.getElementById("root")
);
