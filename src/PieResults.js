// import { useParams } from 'react-router-dom';
// import { useLocation } from 'react-router-dom'
import { Component } from 'react';
import { withRouter } from "react-router-dom";


class PieResults extends Component {
  constructor() {
    super();

    this.state = {loading: true};
  }

  async componentDidMount() {
    const res = await fetch(
      fetch('http://localhost:5000/fetchpies', {
      method: 'POST',
      headers : {
        'Content-Type':'application/json'
      },
      body: JSON.stringify(this.state)
    })
    );

    console.log(res)

    // only make loading false after getting the data from the API
    this.setState({loading: false});
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