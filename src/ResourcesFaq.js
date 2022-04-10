import { Component } from "react";
import Collapsible from "react-collapsible";

class ResourcesFaq extends Component {
  constructor() {
    super();
  }

  render() {
    

    return (
      <div>

        <h1> RESOURCES AND FAQ </h1>

        <Collapsible trigger="What is Apex Fund?" triggerClassName="collapsible" triggerOpenedClassName="collapsible">
          <p className="content"> Answer text here!</p>
        </Collapsible>

        <br/>

        <Collapsible trigger="What is Apex Fund?" triggerClassName="collapsible" triggerOpenedClassName="collapsible">
          <p className="content"> Answer text here!</p>
        </Collapsible>

        <br/>

        <Collapsible trigger="What is Apex Fund?" triggerClassName="collapsible" triggerOpenedClassName="collapsible">
          <p className="content"> Answer text here!</p>
        </Collapsible>

        <br/>

        <Collapsible trigger="Resources" triggerClassName="collapsible" triggerOpenedClassName="collapsible">
          <p className="content"> Put Youtube links here. </p>
        </Collapsible>


      </div>
    )
  }
}

export default ResourcesFaq;