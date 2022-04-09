// import { useParams } from 'react-router-dom';
// import { useLocation } from 'react-router-dom'
import { Component } from 'react';
import { withRouter } from "react-router-dom";


class PieResults extends Component {
  constructor() {
    super();
  }

  render() {
    // console.log(this.props);
    const age = this.props.location.state.age;
    const risk = this.props.location.state.risk;
    const sector = this.props.location.state.sector;
    const userId = this.props.location.state.userId;

    return (
      <div>
        <h1>Age: {age} -- Risk: {risk} -- Sector: {sector} -- User ID: {userId}</h1>
      </div>
    )
  }
}

const PieResultsWithRouter = withRouter(PieResults);

export default PieResultsWithRouter;