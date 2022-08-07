import React, { useState, useEffect } from "react";
import { withRouter } from "react-router-dom";

const PieResults = (props) => {
  const [uid, setUid] = useState(props.location.state.uid);
  const [age, setAge] = useState(props.location.state.age);
  const [risk, setRisk] = useState(props.location.state.risk);
  const [sector, setSector] = useState(props.location.state.sector);

  const [loading, setLoading] = useState(true);
  const [avgBeta, setAvgBeta] = useState();
  const [pie, setPie] = useState();
  const [vizLink, setVizLink] = useState();
  const [username, setUsername] = useState();
  // TODO - storing api keys as state is insecure
  // make it an env variable
  const [apiKey, setApiKey] = useState();
  const [iframe, setIframe] = useState();

  const [numStocks, setNumStocks] = useState();

  useEffect(() => {
    async function fetchPieData() {
      try {
        // TODO: you can call this without await outside of useEffect and mount once the promise resolves
        // you can do you this by providing the variable in a dependency array
        // Send request to backend server to fetch the Pie & Plotly information
        // for the current userId. Wait for the request to give a response.
        const response = await fetch("http://127.0.0.1:5000/fetchpies", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ uid: uid }),
        });

        // removing the `await` here causes the PieReults page to just hang for some reason
        const json = await response.json();

        console.log(json.avgBeta);
        console.log(json.pie);

        // Put all the results from the backend server into our State to be rendered.
        // Remove the loading screen so that the page can finally be rendered.
        setLoading(false);
        setAvgBeta((Math.round(json.avgBeta * 100) / 100).toFixed(2));
        setPie(json.pie);
        setNumStocks(json.pie.length);
        setVizLink(json.vizLink);
        setUsername(json.username);
        setApiKey(json.apiKey);
        setIframe(json.iframe);
      } catch (err) {
        console.log(err);
      }
    }

    fetchPieData();
  }, []);

  if (loading) {
    return <h2>loading ...</h2>;
  }

  console.log("Number of stocks", numStocks);

  return (
    <div>
      {/* Display fields chosen by user in User Form */}
      <h1>
        User ID: {uid}
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
        <p> Overall Beta of Pie: {avgBeta} </p>
        <div />
      </span>

      {/* Embed the Plotly Pie Chart */}
      <div dangerouslySetInnerHTML={{ __html: iframe }} />

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
};

export default withRouter(PieResults);
