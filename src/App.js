import { Component } from "react";
import ReactDOM from "react-dom";
import { StrictMode } from "react";
import apex_logo from "../resources/Apex_Logo_Final.png";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import UserForm from "./UserForm";
import PieResults from "./PieResults";
import ResourcesFaq from "./ResourcesFaq";

class App extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      <div>
        <Router>
          <header>
            <Link to="/">
              <img src={apex_logo} alt="asdf" />
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

            <Route path="/">
              <UserForm />
            </Route>
          </Switch>
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
