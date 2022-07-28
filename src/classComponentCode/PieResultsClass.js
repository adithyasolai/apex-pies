import { Component } from "react";
import { withRouter } from "react-router-dom";

class PieResults extends Component {
  constructor() {
    super();

    this.state = { loading: true };
  }

  // This function is called once when this page is first rendered.
  // This function facilitates when the "Loading..." screen should stay up
  // and when it should be replaced with the actual Pie Results content.
  // This is done by sending a POST request to our backend for information
  // on this user's Pies, and waiting for that POST request to finish.
  async componentDidMount() {
    try {
      // Send request to backend server to fetch the Pie & Plotly information
      // for the current userId. Wait for the request to give a response.
      const response = await fetch("http://127.0.0.1:5000/fetchpies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ uid: this.props.location.state.uid }),
      });

      // removing the `await` here causes the PieReults page to just hang for some reason
      const json = await response.json();

      console.log(json.avgBeta);
      console.log(json.pie);

      // Put all the results from the backend server into our State to be rendered.
      // Remove the loading screen so that the page can finally be rendered.
      this.setState(
        // a fast way of just putting all the API's return values into the state of this component instead of manually typing out
        // each field (name, image, breed, location, etc.)
        Object.assign({
          loading: false, // makes the loading screen go away
          avgBeta: (Math.round(json.avgBeta * 100) / 100).toFixed(2),
          pie: json.pie,
          vizLink: json.vizLink,
          username: json.username,
          apiKey: json.apiKey,
          iframe: json.iframe,
        })
      );
    } catch (err) {
      console.log(err);
    }
  }

  render() {
    // loading screen while waiting for backend server to give Pie information
    if (this.state.loading) {
      return <h2>loading ...</h2>;
    }

    const age = this.props.location.state.age;
    const risk = this.props.location.state.risk;
    const sector = this.props.location.state.sector;
    const userId = this.props.location.state.userId;
    const numStocks = Object.keys(this.state.pie).length;
    console.log(this.state);
    console.log("Number of stocks", numStocks);

    return (
      <div>
        {/* Display fields chosen by user in User Form */}
        <h1>
          User ID: {userId}
          <br />
          Age: {age}
          <br />
          Risk: {risk}
          <br />
          Sector: {sector}
        </h1>

        {/* Educational Hovertext for Beta */}
        {/* TODO: Not really clear that this Beta text is hoverable to user. Need to improve the UI. */}
        <span
          className="hovertext"
          data-hover="Beta is a measure of how a stock/portfolio (pie) moves in comparison to the S&P 500. 
                      A beta of 1 means that the pie has the same volatility as the market. A beta of 1.1 means that the pie is 10% more volatile than the market. 
                      This means that it will have 10% more excess returns compared to the market."
        >
          <p> Overall Beta of Pie: {this.state.avgBeta} </p>
          <div />
        </span>

        {/* Embed the Plotly Pie Chart */}
        <div dangerouslySetInnerHTML={{ __html: this.state.iframe }} />

        {/* Lists information about each stock in our Pie */}
        {/* {Array.from(Array(numStocks), (x, i) => i).map((stockIndex) => {
          return (
            <p key={stockIndex}>
              Percentage: {this.state.pie[stockIndex]["Percentage"]}
              {lineBreak}
              Sector: {this.state.pie[stockIndex]["Sector"]}
              {lineBreak}
              Ticker: {this.state.pie[stockIndex]["Ticker"]}
            </p>
          );
        })} */}

        <br />
      </div>
    );
  }
}

const PieResultsWithRouter = withRouter(PieResults);

export default PieResultsWithRouter;
